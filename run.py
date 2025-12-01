from app import create_app, db
from app.models import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # 1. 自动创建数据库表
        db.create_all()

        # 2. 自动创建测试管理员账号 (如果不存在)
        if not User.query.filter_by(username='admin').first():
            print(">>> 初始化管理员账号: admin / 123")
            admin = User(username='admin', password='123')
            db.session.add(admin)
            db.session.commit()

    # 启动服务
    print(">>> 系统启动中: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)