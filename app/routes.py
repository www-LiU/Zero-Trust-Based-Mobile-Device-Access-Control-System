from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app import db
from app.models import User, AccessLog
from app.core import TrustEngine
from user_agents import parse  # 用于指纹识别
import datetime

main_bp = Blueprint('main', __name__)


# --- 工具函数：写日志 ---
def log_action(user_id, action_type, desc):
    log = AccessLog(user_id=user_id, action_type=action_type, description=desc)
    db.session.add(log)
    db.session.commit()


# --- 页面路由 ---

@main_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            session['username'] = user.username

            # 登录时记录一次设备信息
            ua = parse(request.headers.get('User-Agent', ''))
            log_action(user.id, 'normal', f"设备接入: {ua.os.family} / {ua.browser.family}")
            return redirect(url_for('main.dashboard'))

        return render_template('login.html', error="用户名或密码错误")
    return render_template('login.html')


@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('main.login'))

    # --- 1. 实时采集设备指纹 (演示亮点) ---
    ua_string = request.headers.get('User-Agent', '')
    user_agent = parse(ua_string)
    device_fingerprint = {
        "ip": request.remote_addr,
        "os": f"{user_agent.os.family} {user_agent.os.version_string}",
        "browser": f"{user_agent.browser.family} {user_agent.browser.version_string}",
        "type": "Mobile" if user_agent.is_mobile else "PC/Desktop",
        "ua_raw": ua_string[:40] + "..."
    }

    # --- 2. 调用零信任引擎计算分数 ---
    score, risk_factors = TrustEngine.calculate_score(session['user_id'], session)
    policy, policy_msg = TrustEngine.get_policy(score)

    # --- 3. 执行策略 ---
    if policy == "DENY":
        # 熔断拦截页面
        return render_template('dashboard.html',
                               score=score,
                               status="BLOCKED",
                               device=device_fingerprint,
                               logs=risk_factors,
                               msg="⛔ 连接已被网关自动熔断")

    if policy == "MFA" and not session.get('mfa_passed'):
        # 强制跳转 MFA
        return redirect(url_for('main.mfa_verify'))

    # 正常访问页面
    return render_template('dashboard.html',
                           score=score,
                           status="ACTIVE",
                           device=device_fingerprint,
                           logs=risk_factors,
                           msg=policy_msg,
                           username=session['username'])


@main_bp.route('/mfa', methods=['GET', 'POST'])
def mfa_verify():
    if 'user_id' not in session: return redirect(url_for('main.login'))

    if request.method == 'POST':
        if request.form.get('code') == '1234':  # 演示固定验证码
            session['mfa_passed'] = True
            log_action(session['user_id'], 'normal', "MFA 身份验证通过")
            return redirect(url_for('main.dashboard'))
        else:
            return render_template('mfa.html', error="验证码错误")

    # 获取当前分数用于展示
    score, _ = TrustEngine.calculate_score(session['user_id'], session)
    return render_template('mfa.html', score=score)


@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))


# --- 4. 演示控制接口 (API) ---
@main_bp.route('/api/simulate/<action>')
def simulate(action):
    if 'user_id' not in session: return jsonify({})
    uid = session['user_id']

    if action == 'risk_wifi':
        session['env_risk'] = True  # 标记 session 为不安全
        log_action(uid, 'risk', "网络切换至高风险公共 Wi-Fi")

    elif action == 'attack_sql':
        log_action(uid, 'attack', "检测到 SQL 注入特征流量")

    elif action == 'reset':
        session.pop('env_risk', None)
        session.pop('mfa_passed', None)
        # 清空该用户的日志以恢复 100 分
        AccessLog.query.filter_by(user_id=uid).delete()
        log_action(uid, 'normal', "管理员重置信誉分")
        db.session.commit()

    return jsonify({'status': 'ok'})