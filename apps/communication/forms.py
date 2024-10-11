from flask_wtf.form import FlaskForm

from wtforms import PasswordField, StringField, SubmitField, BooleanField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, length


class FollowForm(FlaskForm):
    submit = SubmitField('フォローする')

class UnfollowForm(FlaskForm):
    submit = SubmitField('フォローを解除する')

class BoardForm(FlaskForm):
    title = StringField(
        "タイトル",
        validators=[
            DataRequired(message="タイトルは必須です。"),
            length(max=50, message="50文字以内で入力してください。"),
        ],
    )
    body = TextAreaField(
        "本文",
        validators=[
            DataRequired(message="本文は必須です。"),
        ],
    )
    submit = SubmitField('投稿')


class CommentForm(FlaskForm):
    body = TextAreaField(
        "本文",
        validators=[
            DataRequired(message="本文は必須です。"),
        ],
    )
    submit = SubmitField('送信')


class ChatForm(FlaskForm):
    message_body = TextAreaField(
        '', 
        validators=[
            DataRequired(message="本文は必須です."),
            ],
        )
    submit = SubmitField()

