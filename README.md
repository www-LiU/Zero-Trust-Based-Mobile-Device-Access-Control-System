
🛡️ Zero Trust Access Control System (基于零信任的设备接入控制系统)

📖 项目简介

本项目是一个基于 零信任架构 (Zero Trust Architecture) 的移动设备接入认证系统原型。与传统的边界防御（VPN/防火墙）不同，本系统不预设任何内部设备是可信的。

系统通过动态信誉评分引擎，实时采集设备指纹（Device Fingerprinting）、分析用户行为（User Behavior Analytics）和环境上下文，动态调整访问权限。支持 ABAC (基于属性的访问控制) 策略，实现从“完全信任”到“MFA二次验证”再到“熔断阻断”的动态防御。

✨ 核心功能亮点

🔍 自动化设备指纹采集

不再依赖用户手动输入，系统自动解析 HTTP 头部信息。

实时提取 IP地址、操作系统、浏览器内核、设备类型 等特征。

在仪表盘中实时展示当前接入设备的完整画像。

🧠 动态信誉评分引擎 (Trust Engine)

核心算法：基于历史行为日志 + 当前环境风险进行加权计算。

实时性：每次请求都会重新计算分值，分值变化毫秒级生效。

评分逻辑：

SQL注入攻击：大幅扣分 (-30)

高风险网络环境：中度扣分 (-25)

正常访问：保持满分 (100)

🚦 自适应访问控制策略 (Adaptive Policy)

🟢 > 80分：信任等级高，允许无感访问。

🟡 50 - 80分：信任等级下降，强制触发 MFA (多因素认证) 页面。

🔴 < 50分：信任崩塌，触发熔断机制，直接拒绝访问。

📊 可视化监控大屏

集成 ECharts 仪表盘，动态展示信誉分变化。

实时审计日志流，高亮显示异常行为。

内置 攻击模拟器，可一键演示“环境切换”和“网络攻击”场景。

🛠️ 技术栈

后端：Python 3.x, Flask (Web框架), SQLAlchemy (ORM)

数据库：SQLite (轻量级，无需配置，开箱即用)

前端：HTML5, Bootstrap 5 (响应式布局), ECharts 5 (数据可视化)

工具库：user-agents (指纹识别)

🚀 快速启动
1. 环境准备

确保本地已安装 Python 3.8 或以上版本。

2. 安装依赖

在项目根目录下运行：

code
Bash
download
content_copy
expand_less
pip install -r requirements.txt
3. 启动系统

运行启动脚本，系统将自动初始化数据库并创建管理员账号：

code
Bash
download
content_copy
expand_less
python run.py
4. 访问系统

打开浏览器访问：http://127.0.0.1:5000

默认管理员账号：admin

默认密码：123


📂 项目结构
code
Text
download
content_copy
expand_less
ZeroTrustDemo/
├── app/
│   ├── __init__.py       # Flask 应用工厂
│   ├── models.py         # 数据库模型 (User, AccessLog)
│   ├── core.py           # 核心算法 (TrustEngine)
│   ├── routes.py         # 业务逻辑与 API
│   └── templates/        # 前端页面
│       ├── dashboard.html # 核心演示大屏
│       ├── login.html     # 登录页
│       └── mfa.html       # MFA 验证页
├── zerotrust.db          # 自动生成的 SQLite 数据库
├── config.py             # 项目配置
├── run.py                # 启动入口
└── requirements.txt      # 依赖列表
📝 理论模型参考

本项目实现了 NIST SP 800-207 (零信任架构标准) 中的核心逻辑组件：

PDP (Policy Decision Point): TrustEngine 类，负责计算分数并决定策略。

PEP (Policy Enforcement Point): Flask 的路由拦截器，负责执行通过、MFA 或 阻断。

🤝 贡献与改进

目前项目为演示原型 (Prototype)，未来可改进方向：

接入 Redis 实现分布式 Session 存储。

对接真实的 LDAP/Active Directory 用户库。

增加流量层面的 AI 异常检测模型。

Created for Course Design Demonstration.