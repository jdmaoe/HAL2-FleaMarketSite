from flask_wtf.file import (
    FileAllowed,
    FileField,
    FileRequired,
    )
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import (
    SubmitField,
    StringField,
    TextAreaField,
    )
from wtforms import IntegerField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, length, NumberRange, InputRequired, ValidationError,Regexp

def allowed_file(form, field):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    if field.data:
        filename = field.data.filename
        if not '.' in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            raise ValidationError('サポートされていない画像形式です。')


class ImageForm(FlaskForm):
    image = FileField('Image', validators=[FileRequired(), allowed_file])



class SellItemForm(FlaskForm):
    firstcategory = SelectField('第一カテゴリ',
                                coerce=int,
                                validators=[DataRequired("一次カテゴリーを指定してください。")]
                                )
    secondcategory = SelectField('第二カテゴリ',
                                 coerce=int,
                                 validators=[DataRequired("二次カテゴリーを指定してください。")]
                                 )
    thirdcategory = SelectField('第三カテゴリ',
                                coerce=int,
                                validators=[DataRequired("三次カテゴリーを指定してください。")]
                                )
    name = StringField(
        validators=[
            DataRequired("商品名を入力してください。"),
            length(max=50, message="50文字以内で入力してください。"),
        ]
    )
    description = TextAreaField(
        validators=[
            DataRequired("商品の説明を入力してください。"),
            length(max=500, message="500文字以内で入力してください。"),
        ]
    )
    price = IntegerField(
        validators=[
            DataRequired("価格を入力してください。"),
            NumberRange(min=1, message="1以上の数値を入力してください。"),
        ]
    )
    condition = SelectField('商品の状態',
                            coerce=int,
                            validators=[DataRequired("商品の状態を選択してください。"),
                                        ]
                            )
    postage = IntegerField('送料',
                           validators=[InputRequired("送料を入力してください。"), NumberRange(min=0, message="0以上の数値を入力してください。"),])

    images = FieldList(
    FormField(ImageForm),
    min_entries=1,
    validators=[DataRequired("画像を選択してください。")]
)
    movie = FileField(
        'Movie',
        validators=[
            FileAllowed(['mp4'], '投稿形式はmp4のみです')
            ]
    )

    submit = SubmitField("出品する")


class CategorySerchForm(FlaskForm):
    firstcategory = SelectField('第一カテゴリ',
                                coerce=int,
                                )
    secondcategory = SelectField('第二カテゴリ',
                                 coerce=int,
                                 )
    thirdcategory = SelectField('第三カテゴリ',
                                coerce=int,
                                )
    #min_price = IntegerField("最低価格")
    #最低価格の設定、1以上の数値を入力してください
    min_price = IntegerField("最低価格", validators=[NumberRange(min=1, message="1以上の数値を入力してください。")])
    max_price = IntegerField("最高価格", validators=[NumberRange(min=1, message="1以上の数値を入力してください。")])
    keyword = StringField("キーワード")
    submit = SubmitField("検索する")
