from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from flask_mail import Message


# Blueprintでmypageアプリを生成する
support = Blueprint(
  'support',
  __name__,
  template_folder='templates',
  static_folder='static'
  )

# topicsページのルーティング
@support.route('/topics')
def topics():
    return render_template('support/topics.html')


# contactページのルーティング
@support.route('/contact')
def contact():
    # もしログインしていれば、フォームの初期値を設定する
    if current_user.is_authenticated:
        name = current_user.username
        email = current_user.email
        return render_template('support/contact.html', name=name, email=email)
    return render_template('support/contact.html')


# contact/confirmのルーティング
@support.route('/contact/confirm', methods=['POST'])
def contact_confirm():
    if request.method == 'POST':
        # フォームからの入力値を取得する
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        return render_template('support/contact_confirm.html', name=name, email=email, message=message)


# contact/completeのルーティング
@support.route('/contact/complete', methods=['POST'])
def contact_complete():
    if request.method == 'POST':
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # フォームからの入力値を取得する
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print("bbbbbbbbbbbbbbbbbbbbbbbb")
        # メールを送信する
        msg = Message(
            'お問い合わせありがとうございます',
            sender='schola.team.j@gmail.com',
            recipients=[email],
        )
        msg.body = f'''
        {name} 様

        お問い合わせありがとうございます。
        以下の内容でお問い合わせを受け付けました。

        {message}
        '''
        print("ccccccccccccccccccccccccccccccccccc")
        current_app.mail.send(msg)

        return render_template('support/contact_complete.html', name=name, email=email, message=message)