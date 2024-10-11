from pathlib import Path
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_mail import Mail
from apps.config import config

# SQLAlchemyインスタンスを作成する
db = SQLAlchemy()
csrf = CSRFProtect()

# LoginManagerインスタンスを作成する
login_manager = LoginManager()

# login_view属性に未ログイン時にリダイレクトするエンドポイントを設定する
login_manager.login_view = "auth.signup"
# login_message属性にログイン後に表示するメッセージを指定する
# ここでは何も表示しないよう空を指定する
login_manager.login_message = ""


# create_app関数を作成する
def create_app(config_key):
    # Flaskインスタンスを作成する
    app = Flask(__name__)

    # config_keyにマッチする環境のコンフィグクラスを読み込む
    app.config.from_object(config[config_key])

    # アプリのコンフィグを設定する
    app.config.from_mapping(
        SECRET_KEY='secret_key',
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent/'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # SQLをコンソールログに出力する設定
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY='secret_key'
    )

    # Mailクラスのコンフィグを設定する
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "schola.team.j@gmail.com"
    app.config["MAIL_PASSWORD"] = "oplj hgrz ykng baet"
    app.config["MAIL_DEFAULT_SENDER"] = "Schola <schola.team.j@gmail.com>"

    # Mailクラスのインスタンスを作成する
    mail = Mail(app)

    # Mailクラスのインスタンスをアプリケーションと連携する
    app.mail = mail

    # SQLAlchemyを初期化する
    db.init_app(app)
    # Migrateを初期化する
    Migrate(app, db)
    csrf.init_app(app)

    # LoginManagerをアプリケーションと連携する
    login_manager.init_app(app)

    # mypageパッケージからviewsをimportする
    from apps.mypage import views as mypage_views

    # register_blueprintを使いviewsのmypageをアプリへ登録する
    app.register_blueprint(mypage_views.mypage, url_prefix="/mypage")

    # authパッケージからviewsをimportする
    from apps.auth import views as auth_views

    # register_blueprintを使いviewsのauthをアプリへ登録する
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    # itemパッケージからviewsをimportする
    from apps.item import views as item_views

    # register_blueprintを使いviewsのitemをアプリへ登録する
    app.register_blueprint(item_views.items)

    # communicationパッケージからviewsをimportする
    from apps.communication import views as communication_views

    # register_blueprintを使いviewsのcommunicationをアプリへ登録する
    app.register_blueprint(communication_views.communication, url_prefix="/communication")

    # specialパッケージからviewsをimportする
    from apps.special import views as special_views

    # register_blueprintを使いviewsのspecialをアプリへ登録する
    app.register_blueprint(special_views.special, url_prefix="/special")

    # supportパッケージからviewsをimportする
    from apps.support import views as support_views

    # register_blueprintを使いviewsのsupportをアプリへ登録する
    app.register_blueprint(support_views.support, url_prefix="/support")

    # set optional bootswatch theme
    app.config['FLASK_ADMIN_SWATCH'] = 'readable'

    admin = Admin(app, name='DB管理', template_mode='bootstrap3')

    # モデルをインポートする
    from apps.mypage.models import User, TradingMessage
    from apps.mypage.models import UserPayment
    from apps.item.models import Item
    from apps.item.models import FirstCategory
    from apps.item.models import SecondCategory
    from apps.item.models import ThirdCategory
    from apps.item.models import ItemCondition
    from apps.item.models import ItemImage
    from apps.item.models import Image
    from apps.item.models import PaymentMethod
    from apps.item.models import Purchase
    from apps.item.models import CreditCardPay
    from apps.item.models import AccountTransferPay
    from apps.mypage.models import Blog
    from apps.communication.models import Follow
    from apps.communication.models import Board
    from apps.communication.models import Comment
    from apps.communication.models import Chat

    class FirstCategoryView(ModelView):
        column_list = ('id', 'name')
        form_columns = ('name',)

    class SecondCategoryView(ModelView):
        column_list = ('id', 'name', 'FirstCategory')
        form_columns = ('name', 'FirstCategory')

    class ThirdCategoryView(ModelView):
        column_list = ('id', 'name', 'SecondCategory')
        form_columns = ('name', 'SecondCategory')

    class ItemConditionView(ModelView):
        column_list = ('id', 'name')
        form_columns = ('name',)

    class ItemView(ModelView):
        column_list = ('id', 'name', 'description', 'price', 'FirstCategory', 'SecondCategory', 'ThirdCategory', 'status', 'created_at')
        form_columns = ('name', 'description', 'price', 'FirstCategory', 'SecondCategory', 'ThirdCategory', 'status', 'created_at')

    class PaymentMethodView(ModelView):
        column_list = ('id', 'name')
        form_columns = ('name',)

    class TradingMessageView(ModelView):
        column_list = ('id', 'message', 'item_id', 'user_id')
        form_columns = ('message', 'item_id', 'user_id')

    class BlogView(ModelView):
        column_list = ('id', 'title', 'body', 'user_id')
        form_columns = ('title', 'body', 'user_id')

    class FollowView(ModelView):
        column_list = ('id', 'follower_id', 'followee_id', 'created_at')
        form_columns = ('follower_id', 'followee_id')

    class BoardView(ModelView):
        column_list = ('id', 'title', 'body', 'user_id')
        form_columns = ('title', 'body', 'user_id')

    class CommentView(ModelView):
        column_list = ('id', 'body', 'user_id', 'board_id')
        form_columns = ('body', 'user_id', 'board_id')

    class ChatView(ModelView):
        column_list = ('id', 'sender_id', 'receiver_id', 'body', 'created_at')
        form_columns = ('sender_id', 'receiver_id', 'body')

    class UserPaymentView(ModelView):
        column_list = ('id', 'user_id', 'payment_method_id', 'u_cardnumber', 'u_accountnumber', 'updated_at')
        form_columns = ('user_id', 'u_cardnumber', 'u_accountnumber')

    admin.add_view(ModelView(name='User', model=User, session=db.session))
    admin.add_view(ItemView(name='Item', model=Item, session=db.session))
    admin.add_view(FirstCategoryView(name='FirstCategory', model=FirstCategory, session=db.session))
    admin.add_view(SecondCategoryView(name='SecondCategory', model=SecondCategory, session=db.session))
    admin.add_view(ThirdCategoryView(name='ThirdCategory', model=ThirdCategory, session=db.session))
    admin.add_view(ItemConditionView(name='ItemCondition', model=ItemCondition, session=db.session))
    admin.add_view(ModelView(name='ItemImage', model=ItemImage, session=db.session))
    admin.add_view(ModelView(name='Image', model=Image, session=db.session))
    admin.add_view(PaymentMethodView(name='PaymentMethod', model=PaymentMethod, session=db.session))
    admin.add_view(ModelView(name='Purchase', model=Purchase, session=db.session))
    admin.add_view(ModelView(name='CreditCardPay', model=CreditCardPay, session=db.session))
    admin.add_view(ModelView(name='AccountTransferPay', model=AccountTransferPay, session=db.session))
    admin.add_view(TradingMessageView(name='TradingMessage', model=TradingMessage, session=db.session))
    admin.add_view(BlogView(name='Blog', model=Blog, session=db.session))
    admin.add_view(FollowView(name='Follow', model=Follow, session=db.session))
    admin.add_view(BoardView(name='Board', model=Board, session=db.session))
    admin.add_view(CommentView(name='Comment', model=Comment, session=db.session))
    admin.add_view(ChatView(name='Chat', model=Chat, session=db.session))
    admin.add_view(UserPaymentView(name='UserPayment', model=UserPayment, session=db.session))

    # 404エラーが発生した際に指定したHTMLを返す
    app.register_error_handler(404, page_not_found)
    # 500エラーが発生した際に指定したHTMLを返す
    app.register_error_handler(500, internal_server_error)

    return app


# 登録したエンドポイント名の関数を作成し、404や500が発生した際に指定したHTMLを返す
def page_not_found(e):
    """404 Not Found"""
    return render_template('404.html'), 404


def internal_server_error(e):
    """500 Internal Server Error"""
    return render_template('500.html'), 500