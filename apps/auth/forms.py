from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SignUpForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired("ユーザ名は必須です。"),
            Length(1, 30, "30文字以内で入力してください。"),
        ],
    )
    email = EmailField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレスの形式で入力してください。"),
        ],
    )
    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired("パスワードは必須です。"),
            validators.EqualTo("re_password", "パスワードが一致しません。"),
            ],
            )
    re_password = PasswordField("パスワード（確認）")
    submit = SubmitField("新規登録")


class LoginForm(FlaskForm):
    email = EmailField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレスの形式で入力してください。"),
        ],
    )
    password = PasswordField("パスワード", validators=[DataRequired("パスワードは必須です。")])
    submit = SubmitField("ログイン")
    submit_f = SubmitField("顔認証")
