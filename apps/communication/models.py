from datetime import datetime

from apps.app import db


class Follow(db.Model):
    __tablename__ = 'follow'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    followee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)


class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text)
    board_activate = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # Userモデルとのリレーションを定義する
    user = db.relationship("User", back_populates="boards", lazy=True)
    # Commentモデルとのリレーションを定義する
    comments = db.relationship("Comment", back_populates="board", lazy=True)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # Userモデルとのリレーションを定義する
    user = db.relationship("User", back_populates="comments", lazy=True)
    # Boardモデルとのリレーションを定義する
    board = db.relationship("Board", back_populates="comments", lazy=True)


class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    #送信者と受信者の区別
    #sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    #receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

