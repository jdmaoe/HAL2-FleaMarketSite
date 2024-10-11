from datetime import datetime

from apps.app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from apps.item.models import Item
from apps.communication.models import Follow


# db.Modelを継承したUserクラスを作成する
class User(db.Model, UserMixin):
    # テーブル名を指定する
    __tablename__ = "users"

    # カラムを定義する
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True)
    email = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(20))
    tel = db.Column(db.String(20), nullable=True)
    postcode = db.Column(db.String(8), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    building_name_number = db.Column(db.String(50), nullable=True)
    face_image_path = db.Column(db.String(50), nullable=True)
    user_activate = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # Blogとのリレーションを定義する
    blogs = db.relationship("Blog", back_populates="user", lazy=True)
    # Followとのリレーションを定義する
    followers = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref='follower', lazy='dynamic')
    followees = db.relationship('Follow', foreign_keys=[Follow.followee_id], backref='followee', lazy='dynamic')
    # Boardとのリレーションを定義する
    boards = db.relationship("Board", back_populates="user", lazy=True)
    # Commentとのリレーションを定義する
    comments = db.relationship("Comment", back_populates="user", lazy=True)
    # chatとのリレーション
    send_chat = db.relationship("Chat", foreign_keys='Chat.sender_id', backref='sender', lazy=True)
    receive_chat = db.relationship("Chat", foreign_keys='Chat.receiver_id', backref='receiver', lazy=True)
    # UserPaymentとのリレーションを定義する
    user_payments = db.relationship("UserPayment", back_populates="user", lazy=True)

    # パスワードをセットするためのプロパティ
    @property
    def password(self):
        raise AttributeError("読み取り不可")

    # パスワードをセットするためのセッター関数でハッシュ化したパスワードをセットする
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # パスワードが正しいかどうかをチェックするメソッド
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # メールアドレスを重複チェックするメソッド
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserPayment(db.Model):
    __tablename__ = "user_payments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("users.id"))
    u_cardnumber = db.Column(db.String(16))
    u_goodthru_year = db.Column(db.Integer)
    u_goodthru_month = db.Column(db.Integer)
    u_cardnominee = db.Column(db.String(20))
    u_bankcode = db.Column(db.String(4))
    u_branchcode = db.Column(db.String(3))
    u_deposititem = db.Column(db.String(1))
    u_accountnumber = db.Column(db.String(7))
    u_accountnominee = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # Userモデルとのリレーションを定義する
    user = db.relationship("User", back_populates="user_payments", lazy=True)


class TradingMessage(db.Model):
    __tablename__ = "trading_messages"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.ForeignKey("item.id"))
    user_id = db.Column(db.ForeignKey("users.id"))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.message


class Blog(db.Model):
    __tablename__ = "blogs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("users.id"))
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    image_path = db.Column(db.String)
    blog_activate = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # Userモデルとのリレーションを定義する
    user = db.relationship("User", back_populates="blogs", lazy=True)
