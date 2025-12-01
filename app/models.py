from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False) # 演示用明文存储

class AccessLog(db.Model):
    """记录用户行为，用于动态计算信誉分"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    action_type = db.Column(db.String(20))  # normal, risk, attack
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.now)