from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, length
from flask_wtf.file import (
    FileAllowed,
    FileField,
    FileRequired,
    )
from wtforms.widgets import TextArea


# ユーザー新規作成フォームクラス
class UserForm(FlaskForm):
    # ユーザーフォームのusername属性のラベルとバリデータを設定する
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired(message="ユーザー名は必須です。"),
            length(max=30, message="30文字以内で入力してください。"),
        ],
    )

    # ユーザーフォームemail属性のラベルとバリデータを設定する
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(message="メールアドレスは必須です。"),
            Email(message="メールアドレスの形式で入力してください。"),
        ],
    )

    # ユーザーフォームpassword属性のラベルとバリデータを設定する
    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired(message="パスワードは必須です。"),
            length(max=20, message="20文字以内で入力してください。"),
        ],
    ) 

    # ユーザーフォームsubmitの文言を設定する
    submit = SubmitField("新規登録")


# ユーザー編集フォームクラス
class UserEditForm(FlaskForm):
    # ユーザーフォームのusername属性のラベルとバリデータを設定する
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired(message="ユーザー名は必須です。"),
            length(max=30, message="30文字以内で入力してください。"),
        ],
    )

    # ユーザーフォームemail属性のラベルとバリデータを設定する
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(message="メールアドレスは必須です。"),
            Email(message="メールアドレスの形式で入力してください。"),
        ],
    )

    # ユーザーフォームpassword属性のラベルとバリデータを設定する
    password = PasswordField(
        "パスワード",
        validators=[
            length(max=20, message="20文字以内で入力してください。"),
        ],
    )

    # ユーザーフォームtel属性のラベルとバリデータを設定する
    tel = StringField(
        "電話番号",
        validators=[
            length(max=20, message="20文字以内で入力してください。"),
        ],
    )

    # ユーザーフォームaddress属性のラベルとバリデータを設定する
    address = StringField(
        "住所",
        validators=[
            length(max=50, message="50文字以内で入力してください。"),
        ],
    )

    # ユーザーフォームbuilding_name_number属性のラベルとバリデータを設定する
    building_name_number = StringField(
        "建物名・部屋番号",
        validators=[
            length(max=50, message="50文字以内で入力してください。"),
        ],
    )

    face_image = FileField(
        validators=[
            FileAllowed(["png", "jpg", "jpeg"], "サポートされていない画像形式です。"),
        ]
    )
    
    # ユーザーフォームsubmitの文言を設定する
    submit = SubmitField("新規登録")


# textareaの改行を<br>に変換する
class CustomTextArea(TextArea):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].replace('\r\n', '<br>').replace('\n', '<br>')


# 取引メッセージフォームクラス
class TradingMessageForm(FlaskForm):
    # 取引連絡フォームのmessage属性のラベルとバリデータを設定する
    message = TextAreaField(
        "メッセージ",
        validators=[
            DataRequired(message="メッセージは必須です。"),
            length(max=100, message="100文字以内で入力してください。"),
        ],
        widget=CustomTextArea(),
    )
    # 取引連絡フォームsubmitの文言を設定する
    submit = SubmitField("送信")


# 発送チェックフォームクラス
class ShippingContactForm(FlaskForm):
    # チェックボックスのラベルを設定する
    shipping_contact = BooleanField("発送済みにする", false_values=None)
    # 発送チェックフォームsubmitの文言を設定する
    submit = SubmitField("発送済みにする")


# 受取チェックフォームクラス
class ReceiptContactForm(FlaskForm):
    # チェックボックスのラベルを設定する
    receipt_contact = BooleanField("受取完了にする", false_values=None)
    # 受取チェックフォームsubmitの文言を設定する
    submit = SubmitField("受取完了にする")


# ブログフォームクラス
class BlogForm(FlaskForm):
    # ブログフォームのtitle属性のラベルとバリデータを設定する
    title = StringField(
        "タイトル",
        validators=[
            DataRequired(message="タイトルは必須です。"),
            length(max=50, message="50文字以内で入力してください。"),
        ],
    )

    # ブログフォームのcontent属性のラベルとバリデータを設定する
    body = TextAreaField(
        "内容",
        validators=[
            DataRequired(message="内容は必須です。"),
            length(max=500, message="500文字以内で入力してください。"),
        ],
    )

    # image = FileField(
    #     validators=[
    #         FileRequired("画像ファイルを指定してください。"),
    #         FileAllowed(["png", "jpg", "jpeg"], "サポートされていない画像形式です。"),
    #     ]
    # )
    image = FileField('画像ファイル')

    # ブログフォームsubmitの文言を設定する
    submit = SubmitField("投稿する")


# ブログ削除フォームクラス
class BlogDeleteForm(FlaskForm):
    # ブログ削除フォームsubmitの文言を設定する
    submit = SubmitField("削除する")
