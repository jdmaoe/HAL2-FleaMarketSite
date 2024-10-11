from apps.app import db
from apps.auth.forms import SignUpForm, LoginForm
from apps.mypage.models import User
from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app, Response
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
import atexit

# 画像処理用ライブラリ
import cv2
import face_recognition
import numpy as np

# Blueprintを使ってauthを生成する
auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static"
    )


video_capture = cv2.VideoCapture(0)


def gen_frames():
    while True:
        # ビデオキャプチャからフレームを取得する
        success, frame = video_capture.read()
        if not success:
            break
        # 顔認識を行う
        ret, buffer = cv2.imencode('.jpg', frame)
        # フレームをバイト型に変換する
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def load_known_faces():
    #users = User.query.all()
    users = User.query.order_by(User.id.desc()).all()
    known_faces_paths = []
    for user in users:
        if user.face_image_path is None:
            # リストに登録されないidと名前をprint
            print("ノウンフェイスに追加されないユーザーIDは",user.id,"ユーザー名は",user.username)
            continue
        known_faces_paths.append("apps/images/"+str(user.face_image_path))
        # リストに追加されるidと名前をprint
        print("ノウンフェイスに追加されるユーザーIDは",user.id,"ユーザー名は",user.username)
    known_faces = []
    for face_path in known_faces_paths:
        face_image = face_recognition.load_image_file(face_path)
        face_locations = face_recognition.face_locations(face_image)

        if face_locations:
            face_encoding = np.mean(face_recognition.face_encodings(face_image, face_locations), axis=0)
            known_faces.append(face_encoding)
    return known_faces

def cleanup():
    video_capture.release()
    cv2.destroyAllWindows()

@auth.route('/face')
def face():
    return render_template('auth/face.html')


@auth.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@auth.route('/result')
def result():

    known_faces = load_known_faces()

    def recognize_face(frame):
        face_locations = face_recognition.face_locations(frame)
        recognition_result = None
        # 顔が検出された場合
        if len(face_locations) > 0:
            # 顔の特徴量を取得する
            face_encoding = np.mean(face_recognition.face_encodings(frame, face_locations), axis=0)
            # 顔の特徴量と既知の顔の特徴量を比較する
            for i, known_face in enumerate(known_faces):
                # iはknown_facesのindex
                # 照合中のindexをprint
                print("照合中のknown_facesのindexは",i)
                # 顔の特徴量が一致した場合,resultにTrueが入る
                results = face_recognition.compare_faces([known_face], face_encoding, tolerance=0.4)
                # Trueが一つでもあれば認識成功
                if results[0]:
                    # known_faces_pathsをload_known_faces関数内から取得
                    # users = User.query.all()
                    # Userを逆順に取得
                    users = User.query.order_by(User.id.desc()).all()
                    # User.idを順番にprint
                    known_faces_paths = []
                    for user in users:
                        if user.face_image_path is None:
                            continue
                        known_faces_paths.append("apps/images/"+str(user.face_image_path))
                    recognition_result = f"認識成功！"
                    # known_faces_paths[i]からapps/images/を削除
                    known_faces_paths[i] = known_faces_paths[i].replace("apps/images/", "")
                    # 顔認証に成功したユーザーをログインさせる
                    user = User.query.filter_by(face_image_path=known_faces_paths[i]).first()
                    # 認証に成功したユーザーのIDと名前をprint
                    print("認証に成功したユーザーのIDは",user.id,"ユーザー名は",user.username)
                    login_user(user)

                    break
            else:
                recognition_result = "認識失敗"
        else:
            recognition_result = "顔が検出されません"

        return recognition_result

    recognition_result = recognize_face(video_capture.read()[1])
    atexit.register(cleanup)

    # return render_template('auth/result.html', recognition_result=recognition_result)
    # 顔認証に成功した場合はface_login_success.htmlにリダイレクトする
    if recognition_result == "認識成功！":
        return redirect(url_for('auth.face_login_success'))
    elif recognition_result == "認識失敗":
        return redirect(url_for('auth.face_login_fail'))
    else:
        return redirect(url_for('auth.face_login_not_detected'))


# 顔認証用のログイン画面を作成する
@auth.route("/face_login", methods=["GET"])
def face_login():
    return redirect(url_for('mypage.profile', user_id=current_user.id))


# 顔認証成功ページを作成する
@auth.route("/face_login_success", methods=["GET"])
@login_required
def face_login_success():
    return render_template("auth/face_login_success.html")

# 顔認識に失敗した場合のページを作成する
@auth.route("/face_login_fail", methods=["GET"])
def face_login_fail():
    return render_template("auth/face_login_fail.html")

# 顔認識で未検出の場合のページを作成する
@auth.route("/face_login_not_detected", methods=["GET"])
def face_login_not_detected():
    return render_template("auth/face_login_not_detected.html")

# ログイン/新規登録画面を作成する
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # SignUpFormをインスタンス化する
    form_s = SignUpForm()
    form = LoginForm()
    # POSTの場合はログイン処理を行う
    if form.validate_on_submit():
        # もしuserのuser_activeがFalseの場合はログインできない
        user = User.query.filter_by(email=form.email.data).first()
        # userが存在しない場合はログインできない
        if user is None:
            flash("メールアドレスかパスワードが間違っています。")
            return redirect(url_for("auth.signup"))
        if user.user_activate == False:
            flash("このユーザーは退会済みです。")
            return redirect(url_for("auth.signup"))
        # user_activateがTrueで、ユーザーが存在し、パスワードが正しい場合はログインする
        elif user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("items.index"))
        # ログイン失敗メッセージを表示する
        flash("メールアドレスかパスワードが間違っています。")
        return render_template("auth/signup.html", form_s=form_s, form=form)
    # GETの場合はsignup.htmlを表示する
    return render_template("auth/signup.html", form_s=form_s, form=form)


# 新規登録のエンドポイントを作成する
@auth.route("/register", methods=["POST"])
def register():
    # SignUpFormをインスタンス化する
    form_s = SignUpForm()
    # 入力されたパスワードと確認用パスワードが一致するかチェックする
    if form_s.password.data != form_s.re_password.data:
        flash("パスワードが一致しません。")
        return redirect(url_for("auth.signup"))
    # ユーザー情報を登録する
    user = User(
        username=form_s.username.data,
        email=form_s.email.data,
        password=form_s.password.data,
    )
    # メールアドレス重複チェックをする
    if user.is_duplicate_email():
        flash("指定のメールアドレスは登録済みです")
        return redirect(url_for("auth.signup"))
    # ユーザー情報を登録する
    db.session.add(user)
    db.session.commit()
    # flashメッセージを表示する
    flash("ユーザー登録が完了しました。")
    return redirect(url_for("auth.signup"))


# ログアウト画面のエンドポイントを作成する
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.signup"))


# パスワード再設定メール送信画面のエンドポイントを作成する
@auth.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form["email"]
        # メールアドレスでユーザーを検索する
        user = User.query.filter_by(email=email).first()
        # ユーザーが存在しない場合はログインページへリダイレクトする
        if user is None:
            flash("メールアドレスが間違っています。")
            return redirect(url_for("auth.reset_password"))
        # メールを送信する
        msg = Message(
            subject="パスワード再設定",
            sender="schola.team.j@gmail.com",
            recipients=[email],
        )
        # user.password_hashをmsg.bodyにセットする
        msg.body = f"""
        以下のURLからパスワードを再設定してください。
        http://localhost:5000/auth/reset_password_form/{user.password_hash}
        """
        # メールを送信する
        current_app.mail.send(msg)
        flash("パスワード再設定用のメールを送信しました。")
        return redirect(url_for("auth.reset_password"))

    return render_template("auth/reset_password.html")


# パスワード再設定画面のエンドポイントを作成する
@auth.route("/reset_password_form/<password_hash>", methods=["GET"])
def reset_password_form(password_hash):
    form = SignUpForm()
    return render_template("auth/reset_password_form.html", form=form, password_hash=password_hash)


# パスワード再設定完了画面のエンドポイントを作成する
@auth.route("/reset_password_complete", methods=["POST"])
def reset_password_complete():
    # パスワード再設定画面から受け取ったパスワードを取得する
    password = request.form["password"]
    password_hash = request.form["password_hash"]
    # パスワードを更新する
    user = User.query.filter_by(password_hash=password_hash).first()
    user.password = password
    db.session.commit()
    flash("パスワードを再設定しました。")
    return redirect(url_for("auth.signup"))
