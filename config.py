import os


class Config:
    # 演示用密钥，生产环境请生成随机字符串
    SECRET_KEY = 'demo-secret-key-course-design'

    # 数据库配置 (SQLite)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'zerotrust.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False