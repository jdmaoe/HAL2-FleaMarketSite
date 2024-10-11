from apps.app import db
from apps.mypage.models import User, TradingMessage, Blog, UserPayment
from apps.mypage.forms import (
    UserForm,
    UserEditForm,
    TradingMessageForm,
    ShippingContactForm,
    ReceiptContactForm,
    BlogForm,
    BlogDeleteForm
    )
from apps.item.models import Item, ItemImage, Image, Purchase
from apps.communication.models import Follow
from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from flask_login import login_required, current_user
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import datetime

# Blueprintでmypageアプリを生成する
mypage = Blueprint(
  'mypage',
  __name__,
  template_folder='templates',
  static_folder='static',
  )


# 画像を保存する関数を作成する
def save_image(file):
    if file:
        filename = secure_filename(file.filename)
        ext = Path(filename).suffix
        filename = str(uuid.uuid4()) + ext
        file_path = Path(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        return str(filename)
    return None


# indexエンドポイントを作成しindex.htmlを返す（後で消す）
@mypage.route('/')
@login_required
def index():
    return render_template('mypage/index.html')


# 開発用の実験ページ（後で消す）
@mypage.route('/sql')
@login_required
def sql():
    db.session.query(User).all()
    return "コンソールログを確認してください"



# 各ユーザーのマイページを作成する
@mypage.route("/users/<user_id>")
@login_required
def profile(user_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.profile", user_id=current_user.id))
    elif current_user.id == int(user_id):
        user = User.query.filter_by(id=user_id).first()
        return render_template("mypage/user.html", user=user)

# 各ユーザーの顔画像を変更するエンドポイントを作成する
@mypage.route("/users/face_image/<user_id>", methods=["POST"])
@login_required
def change_face_image(user_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.profile", user_id=current_user.id))
    elif current_user.id == int(user_id):
        user = User.query.filter_by(id=user_id).first()
        # 画像がアップロードされている場合は保存する
        if request.files['face_image']:
            file = request.files['face_image']
            user.face_image_path = save_image(file)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("mypage.profile", user_id=user.id))
        # マイページ編集画面へリダイレクトする
        return redirect(url_for("mypage.edit_user", user_id=user.id))







# 各ユーザーのマイページ編集画面を作成する
# methodsにGETとPOSTを指定する
@mypage.route("/users/profile/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.profile", user_id=current_user.id))
    elif current_user.id == int(user_id):
        # Userモデルを利用してユーザーを取得する
        user = User.query.filter_by(id=user_id).first()
        pay_user = UserPayment.query.filter_by(user_id=user_id).first()

        # ユーザーIDが本人以外の場合はエラーメッセージ表示する
        if current_user.id != user.id:
            return "権限がありません"
        else:
            video_capture = cv2.VideoCapture(0)
            # POSTの場合はフォームから送信された値を取得する
            # formからサブミットされた場合はユーザーを更新し,マイページにリダイレクトする
            if request.method == "POST":
                user.username = request.form["userName"]
                user.email = request.form["email"]
                # パスワードが入力されている場合は更新する
                if request.form["password"]:
                    user.password = request.form["password"]
                user.tel = request.form["tel"]
                user.postcode = request.form["postcode"]
                user.address = request.form["address"]
                user.building_name_number = request.form["building_name_number"]
   
                # 画像がアップロードされている場合は保存する
                if request.files['face_image']:
                    file = request.files['face_image']
                    user.face_image_path = save_image(file)
                if pay_user is None:
                    print(request.form["cardnumber"])
                    print(request.form["goodthru_year"])
                    print(request.form["goodthru_month"])
                    print(request.form["cardnominee"])
                    print(request.form["bankcode"])
                    print(request.form["branchcode"])
                    print(request.form["deposititem"])
                    print(request.form["accountnumber"])
                    print(request.form["accountnominee"])             
                    pay_user = UserPayment(
                        user_id=user_id,
                        u_cardnumber=request.form["cardnumber"],
                        u_goodthru_year=request.form["goodthru_year"],
                        u_goodthru_month=request.form["goodthru_month"],
                        u_cardnominee=request.form["cardnominee"],
                        u_bankcode=request.form["bankcode"],
                        u_branchcode=request.form["branchcode"],
                        u_deposititem=request.form["deposititem"],
                        u_accountnumber=request.form["accountnumber"],
                        u_accountnominee=request.form["accountnominee"],
                    )
                # もしpay_userが存在する場合は更新する
                else:
                    pay_user.u_cardnumber = request.form["cardnumber"]
                    pay_user.u_goodthru_year = request.form["goodthru_year"]
                    pay_user.u_goodthru_month = request.form["goodthru_month"]
                    pay_user.u_cardnominee = request.form["cardnominee"]
                    pay_user.u_bankcode = request.form["bankcode"]
                    pay_user.u_branchcode = request.form["branchcode"]
                    pay_user.u_deposititem = request.form["deposititem"]
                    pay_user.u_accountnumber = request.form["accountnumber"]
                    pay_user.u_accountnominee = request.form["accountnominee"]
                db.session.add(user)
                db.session.add(pay_user)
                db.session.commit()
                flash("変更を登録しました")
                return redirect(url_for("mypage.edit_user", user_id=user.id))

            # GETの場合はHTMLを返す
            return render_template("mypage/edit.html", user=user, pay_user=pay_user)


# 退会処理のエンドポイントを作成する
@mypage.route("/mypage/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.profile", user_id=current_user.id))
    elif current_user.id == int(user_id):
        user = User.query.filter_by(id=user_id).first()
        # Itemのitem_statusの定義は0:出品取消, 1:出品中, 2:発送待ち, 3:受取待ち, 4:受取完了
        # Itemのmovieflagの定義はTrue:動画, False:物品
        # Itemモデルを利用して出品中の商品の内movieflagがFalseのもので、item_statusが1, 2, 3のものを取得する。つまり、取引中の物品がある場合は退会できない。
        items_sell_item = Item.query.filter_by(seller_id=user_id, movieflag=False).filter(Item.status >= 1, Item.status <= 3).all()
        # Itemモデルを利用して購入中の商品の内movieflagがFalseのもので、item_statusが2, 3のものを取得する。つまり、取引中の物品がある場合は退会できない。
        items_buy_item = Item.query.filter_by(buyer_id=user_id, movieflag=False).filter(Item.status >= 2, Item.status <= 3).all()
        # もし、items_sell_item, items_buy_itemのいずれかが存在する場合は、退会できないメッセージを表示する
        if items_sell_item or items_buy_item:
            flash("取引が完了していない商品があります。")
            return redirect(url_for("mypage.edit_user", user_id=user_id))
        else:
            # そうでない場合は、Itemモデルを利用して出品中の商品の内movieflagがTrueのものの内、item_statusが1のものを取得する
            items_sell_movie = Item.query.filter_by(seller_id=user_id, movieflag=True).filter(Item.status == 1).all()
            # movieflagがTrueのものが存在する場合は、item_statusを0に変更する
            for item in items_sell_movie:
                item.status = 0
                db.session.add(item)
                db.session.commit()
            # userのuser_activateをFalseに変更する
            user.user_activate = False
            # userのusernameを"退会したユーザー"に変更する
            user.username = "退会したユーザー"
            db.session.add(user)
            db.session.commit()
            # ログアウトする
            return redirect(url_for("auth.logout"))


# 出品中の商品一覧を表示するエンドポイントを作成
@mypage.route("/listing/<user_id>/", methods=["GET", "POST"])
@login_required
def listing(user_id):
    # Postの場合は商品のステータスを変更する
    if request.method == "POST":
        item_id = request.form["item_id"]
        item = Item.query.filter_by(id=item_id).first()
        item.status = 0
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("mypage.listing", user_id=user_id))
    else:
        # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
        if current_user.id != int(user_id):
            return redirect(url_for("mypage.profile", user_id=current_user.id))
        elif current_user.id == int(user_id):
            # 出品中(item.status=1)で、seller_idがuser_idの商品一覧を表示する
            items = db.session.query(Item, Image).join(ItemImage, Item.id == ItemImage.item_id).join(Image, ItemImage.image_id == Image.id).filter(Item.seller_id == user_id, Item.status == 1).group_by(Item.id).all()
            return render_template("mypage/listing.html", items=items)


# 出品取引中の商品一覧を表示するエンドポイントを作成
@mypage.route("/selltrading/<user_id>/")
@login_required
def selltrading(user_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.profile", user_id=current_user.id))
    elif current_user.id == int(user_id):
        # 出品取引中(item.statusが2～3)の商品一覧を表示する
        items = db.session.query(Item, Image, User).join(ItemImage, Item.id == ItemImage.item_id).join(Image, ItemImage.image_id == Image.id).join(User, Item.buyer_id == User.id).filter(Item.seller_id == user_id, Item.status >= 2, Item.status <= 3).group_by(Item.id).all()
        user = current_user
        return render_template("mypage/selltrading.html", items=items, user=user)


# 出品取引中連絡画面を表示するエンドポイントを作成
@mypage.route("/selltrading/<user_id>/<item_id>/", methods=["GET", "POST"])
@login_required
def selltrading_message(user_id, item_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.profile", user_id=current_user.id))
    elif current_user.id == int(user_id):
        # 出品取引中の商品の情報を取得する
        item = Item.query.filter_by(id=item_id).first()
        # 出品取引中の商品の画像を取得する
        item_images = db.session.query(Image).join(ItemImage, Image.id == ItemImage.image_id).filter(ItemImage.item_id == item_id).all()
        # 出品取引中の商品の購入者の情報を取得する
        buyer = User.query.filter_by(id=item.buyer_id).first()
        # 出品取引中の商品の出品者の情報を取得する
        seller = User.query.filter_by(id=item.seller_id).first()
        user = current_user
        # TradingMessageモデルとUserモデルを利用してメッセージを取得する
        messages = db.session.query(TradingMessage, User).join(User, TradingMessage.user_id == User.id).filter(TradingMessage.item_id == item_id).all()

        form_s = ShippingContactForm()
        form_m = TradingMessageForm()

        # 出品取引中の商品のstatusが2または3でない場合は、出品取引中の商品一覧ページにリダイレクトする
        if item.status != 2 and item.status != 3:
            return redirect(url_for("mypage.selltrading", user_id=user_id))

        # POSTの場合,shipping_contactの値を取得する
        if request.method == "POST":
            shipping_contact = request.form["shipping_contact"]
            # shipping_contactが空でない場合、statusを3に変更する
            if shipping_contact != "":
                item.status = 3
                db.session.add(item)
                db.session.commit()
                return redirect(url_for("mypage.selltrading", user_id=user_id))
            # shipping_contactが空の場合、レンダリングする
            else:
                return render_template("mypage/selltrading_message.html", item=item, buyer=buyer, seller=seller, user=user, form_s=form_s, form_m=form_m, messages=messages, item_images=item_images)
        # GETの場合はHTMLを返す
        else:
            return render_template("mypage/selltrading_message.html", item=item, buyer=buyer, seller=seller, user=user, form_s=form_s, form_m=form_m, messages=messages, item_images=item_images)


# 取引中メッセージを処理するエンドポイントを作成
@mypage.route("/trading_message/<user_id>/<item_id>", methods=["POST"])
@login_required
def trading_message(user_id, item_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.profile", user_id=current_user.id))
    elif current_user.id == int(user_id):
        # Itemモデルを利用して商品を取得する
        item = Item.query.filter_by(id=item_id).first()
        message = request.form["message"]
        print("あああああああああああああああああああああああああ")
        print(message)
        message = message.replace('\r\n', '<br>').replace('\n', '<br>')
        # 取引メッセージを作成する
        trading_message = TradingMessage(
            item_id=item.id,
            user_id=current_user.id,
            message=message,
        )
        # 取引メッセージを追加してコミットする
        db.session.add(trading_message)
        db.session.commit()
        # もしcurrent_userが出品者の場合は、出品取引中連絡画面へリダイレクトする
        if current_user.id == item.seller_id:
            return redirect(url_for("mypage.selltrading_message", user_id=user_id, item_id=item_id))
        # もしcurrent_userが購入者の場合は、購入取引中連絡画面へリダイレクトする
        elif current_user.id == item.buyer_id:
            return redirect(url_for("mypage.buytrading_message", user_id=user_id, item_id=item_id))


# 購入取引中の商品一覧を表示するエンドポイントを作成
@mypage.route("/buytrading/<user_id>/")
@login_required
def buytrading(user_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.profile", user_id=current_user.id))
    elif current_user.id == int(user_id):
        # 購入取引中(item.status=2)の商品一覧を表示する
        items = db.session.query(Item, Image, User).join(ItemImage, Item.id == ItemImage.item_id).join(Image, ItemImage.image_id == Image.id).join(User, Item.seller_id == User.id).filter(Item.buyer_id == user_id, Item.status >= 2, Item.status <= 3).group_by(Item.id).all()
        user = current_user
        return render_template("mypage/buytrading.html", items=items, user=user)


# 購入取引中連絡画面を表示するエンドポイントを作成
@mypage.route("/buytrading/<user_id>/<item_id>/", methods=["GET", "POST"])
@login_required
def buytrading_message(user_id, item_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.profile", user_id=current_user.id))
    elif current_user.id == int(user_id):

        
        item = Item.query.filter_by(id=item_id).first()
        item_images = db.session.query(Image).join(ItemImage, Image.id == ItemImage.image_id).filter(ItemImage.item_id == item_id).all()
        
        # 購入取引中の商品の購入者の情報を取得する
        buyer = User.query.filter_by(id=item.buyer_id).first()
        # 購入取引中の商品の出品者の情報を取得する
        seller = User.query.filter_by(id=item.seller_id).first()
        user = current_user
        # TradingMessageモデルとUserモデルを利用してメッセージを取得する
        messages = db.session.query(TradingMessage, User).join(User, TradingMessage.user_id == User.id).filter(TradingMessage.item_id == item_id).all()

        form_r = ReceiptContactForm()
        form_m = TradingMessageForm()

        # 出品取引中の商品のstatusが2または3でない場合は、出品取引中の商品一覧ページにリダイレクトする
        if item.status != 2 and item.status != 3:
            return redirect(url_for("mypage.buytrading", user_id=user_id))

        # POSTの場合,receipt_contactの値を取得する
        if request.method == "POST":
            receipt_contact = request.form["receipt_contact"]
            # receipt_contactが空でない場合、statusを4に変更する
            if receipt_contact != "":
                item.status = 4
                db.session.add(item)
                db.session.commit()
                return redirect(url_for("mypage.buytrading", user_id=user_id))
            # receipt_contactが空の場合、レンダリングする
            else:
                return render_template("mypage/buytrading_message.html", item=item, buyer=buyer, seller=seller, user=user, form_r=form_r, form_m=form_m, messages=messages, item_images=item_images)
        # GETの場合はHTMLを返す
        else:
            return render_template("mypage/buytrading_message.html", item=item, buyer=buyer, seller=seller, user=user, form_r=form_r, form_m=form_m, messages=messages, item_images=item_images)


# 売却完了の商品一覧を表示するエンドポイントを作成
@mypage.route("/sold/<user_id>/")
@login_required
def sold(user_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.profile", user_id=current_user.id))
    elif current_user.id == int(user_id):
        # 売却完了(item.status=4)の商品一覧を表示する
        items = db.session.query(Item, Image, User).join(ItemImage, Item.id == ItemImage.item_id).join(Image, ItemImage.image_id == Image.id).join(User, Item.buyer_id == User.id).filter(Item.seller_id == user_id, Item.status == 4).group_by(Item.id).all()
        user = current_user
        return render_template("mypage/sold.html", items=items, user=user)


# 購入完了の商品一覧を表示するエンドポイントを作成
@mypage.route("/bought/<user_id>/")
@login_required
def bought(user_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.profile", user_id=current_user.id))
    elif current_user.id == int(user_id):
        # 購入完了(item.status=4)の商品一覧を表示する
        items = db.session.query(Item, Image, User).join(ItemImage, Item.id == ItemImage.item_id).join(Image, ItemImage.image_id == Image.id).join(User, Item.seller_id == User.id).filter(Item.buyer_id == user_id, Item.status == 4).group_by(Item.id).all()
        user = current_user
        return render_template("mypage/bought.html", items=items, user=user)


# 購入した動画一覧を表示するエンドポイントを作成
@mypage.route("/bought_movie/<user_id>/")
@login_required
def bought_movie(user_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.bought_movie", user_id=current_user.id))
    elif current_user.id == int(user_id):
        # PurchaseモデルとItemモデルとItemImageとImageを利用して購入した動画一覧を取得する
        movies = db.session.query(Purchase, Item, ItemImage, Image).join(Item, Purchase.item_id == Item.id).join(ItemImage, Item.id == ItemImage.item_id).join(Image, ItemImage.image_id == Image.id).filter(Purchase.buyer_id == user_id, Item.movieflag == True).group_by(Item.id).all()
        user = current_user
        return render_template("mypage/bought_movie.html", movies=movies, user=user)


# 購入した動画の詳細を表示するエンドポイントを作成
@mypage.route("/bought_movie/<user_id>/<item_id>/")
@login_required
def play_movie(user_id, item_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("/bought_movie/<user_id>/", user_id=current_user.id))
    elif current_user.id == int(user_id):
        # PurchaseモデルとItemモデルを利用して購入した動画の詳細を取得する
        movie = db.session.query(Purchase, Item).join(Item, Purchase.item_id == Item.id).filter(Purchase.buyer_id == user_id, Item.movieflag == True, Item.id == item_id).first()
        user = current_user
        return render_template("mypage/play_movie.html", movie=movie, user=user) 


# ブログ投稿・一覧を表示するエンドポイントを作成
@mypage.route("/blog/<user_id>/", methods=["GET", "POST"])
@login_required
def blog(user_id):
    form = BlogForm()
    form_d = BlogDeleteForm()
    

    # POSTの場合はフォームから送信された値を取得する
    if form.validate_on_submit():
        # アップロードされた画像ファイルを取得する
        file = form.image.data

        # ファイルのファイル名と拡張子を取得し、ファイル名をuuidに変換する
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        # 画像を保存する
        image_path = Path(current_app.config["UPLOAD_FOLDER"], image_uuid_file_name)
        file.save(image_path)
        # ブログを作成する
        blog = Blog(
            title=form.title.data,
            body=form.body.data,
            image_path=image_uuid_file_name,
            user_id=user_id,
        )
        # ブログを追加してコミットする
        db.session.add(blog)
        db.session.commit()
        # ブログ一覧画面へリダイレクトする
        return redirect(url_for("mypage.blog", user_id=user_id))
    # GETの場合はHTMLを返す
    else:
        # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
        if current_user.id != int(user_id):
            return redirect(url_for("mypage.profile", user_id=current_user.id))
        elif current_user.id == int(user_id):
            # Blogの内blog_activateがTrueのもので、user_idが一致するものを逆順にして取得する
            blogs = Blog.query.filter_by(blog_activate=True, user_id=user_id).order_by(Blog.created_at.desc()).all()
            # 現在時刻を取得する
            current_time = datetime.datetime.now()

            user = current_user
            return render_template("mypage/blog.html", blogs=blogs, user=user, form=form, form_d=form_d, current_time=current_time)


# ブログ削除のエンドポイントを作成
@mypage.route("/blog/<user_id>/<blog_id>/delete", methods=["POST"])
@login_required
def delete_blog(user_id, blog_id):
    # Blogモデルを利用してブログを取得する
    blog = Blog.query.filter_by(id=blog_id).first()
    # ブログのblog_activateをFalseに変更する
    blog.blog_activate = False
    db.session.add(blog)
    db.session.commit()
    # ブログ一覧画面へリダイレクトする
    return redirect(url_for("mypage.blog", user_id=user_id))


# ブログ編集のエンドポイントを作成
@mypage.route("/blog/<user_id>/<blog_id>/edit", methods=["GET", "POST"])
@login_required
def edit_blog(user_id, blog_id):
    form = BlogForm()
    user = current_user
    # Blogモデルを利用してブログを取得する
    blog = Blog.query.filter_by(id=blog_id).first()
    # POSTの場合はフォームから送信された値を取得する
    if form.validate_on_submit():
        # アップロードされた画像ファイルを取得する
        file = form.image.data

        # ファイルのファイル名と拡張子を取得し、ファイル名をuuidに変換する
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        # 画像を保存する
        image_path = Path(current_app.config["UPLOAD_FOLDER"], image_uuid_file_name)
        file.save(image_path)
        # ブログを更新する
        blog.title = form.title.data
        blog.body = form.body.data
        blog.image_path = image_uuid_file_name
        # ブログを上書きしてコミットする
        db.session.add(blog)
        db.session.commit()
        # ブログ一覧画面へリダイレクトする
        return redirect(url_for("mypage.blog", user_id=user_id))
    # GETの場合はHTMLを返す
    else:
        # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
        if current_user.id != int(user_id):
            return redirect(url_for("mypage.profile", user_id=current_user.id))
        elif current_user.id == int(user_id):
            # ブログ編集画面をレンダリングする
            return render_template("mypage/edit_blog.html", blog=blog, user=user, form=form)


# フォロー中のユーザー一覧を表示するエンドポイントを作成
@mypage.route("/follow/<user_id>/", methods=["GET", "POST"])
@login_required
def follow_list(user_id):
    # フォロー解除の場合は、フォロー解除する
    if request.method == "POST":
        user_id = request.form["user_id"]
        followee_id = request.form["followee_id"]
        follow = Follow.query.filter_by(follower_id=user_id, followee_id=followee_id).first()
        db.session.delete(follow)
        db.session.commit()
        return redirect(url_for("mypage.follow_list", user_id=user_id))


    else:
        # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
        if current_user.id != int(user_id):
            return redirect(url_for("mypage.profile", user_id=current_user.id))
        elif current_user.id == int(user_id):
            # FollowモデルとUserモデルを利用してフォロー中のユーザー一覧を取得する
            follows = db.session.query(Follow, User).join(User, Follow.followee_id == User.id).filter(Follow.follower_id == user_id).all()
            user = current_user
            return render_template("mypage/follow_list.html", follows=follows, user=user)


# フォロワー一覧を表示するエンドポイントを作成
@mypage.route("/follower/<user_id>/")
@login_required
def follower_list(user_id):
    # もしcurrent_userのidとuser_idが一致しない場合は、マイページにリダイレクトする
    if current_user.id != int(user_id):
        return redirect(url_for("mypage.profile", user_id=current_user.id))
    elif current_user.id == int(user_id):
        # FollowモデルとUserモデルを利用してフォロワー一覧を取得する
        followers = db.session.query(Follow, User).join(User, Follow.follower_id == User.id).filter(Follow.followee_id == user_id).all()
        user = current_user
        return render_template("mypage/follower_list.html", followers=followers, user=user)
