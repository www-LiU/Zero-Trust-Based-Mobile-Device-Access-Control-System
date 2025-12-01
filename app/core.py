from app.models import AccessLog


class TrustEngine:
    """
    零信任核心引擎：基于「持续验证」理念
    每次请求都重新计算用户当前的信誉分
    """
    MAX_SCORE = 100

    @staticmethod
    def calculate_score(user_id, session_context):
        """
        :param user_id: 用户ID
        :param session_context: 当前会话上下文 (如是否在模拟风险环境)
        :return: (分数, 扣分原因列表)
        """
        score = TrustEngine.MAX_SCORE
        logs = AccessLog.query.filter_by(user_id=user_id) \
            .order_by(AccessLog.timestamp.desc()).limit(15).all()

        factors = []

        # --- 1. 行为分析策略 ---
        for log in logs:
            if log.action_type == 'attack':
                score -= 30
                factors.append(f"检测到高危攻击行为: {log.description} (-30)")
            elif log.action_type == 'risk':
                score -= 10
                factors.append(f"存在风险操作: {log.description} (-10)")

        # --- 2. 环境感知策略 (演示模拟) ---
        if session_context.get('env_risk'):
            score -= 25
            factors.append("当前网络环境不可信 (公共Wi-Fi) (-25)")

        # --- 3. 归一化处理 ---
        final_score = max(0, min(100, score))

        return final_score, list(set(factors))  # 去重返回

    @staticmethod
    def get_policy(score):
        """基于分数动态下发策略 (ABAC)"""
        if score >= 80:
            return "ALLOW", "🟢 信任等级高，允许访问"
        elif score >= 50:
            return "MFA", "🟡 信任等级下降，需二次验证"
        else:
            return "DENY", "🔴 信任等级过低，熔断拦截"