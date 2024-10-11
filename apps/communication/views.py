import uuid
from pathlib import Path

from apps.app import db

from flask_login import current_user, login_required
from flask import flash

from apps.mypage.models import User, Blog
from apps.mypage.views import BlogForm
from apps.communication.models import Follow, Board, Comment, Chat
from apps.communication.forms import FollowForm, BoardForm, CommentForm, ChatForm

from flask import (
    Blueprint,
    current_app,
    render_template,
    send_from_directory,
    redirect,
    url_for,
    request,
)

# login_required, current_userをimportする
from flask_login import current_user, login_required
import datetime

# template_folderを指定する
communication = Blueprint(
    'communication',
    __name__,
    template_folder='templates',
    static_folder='static',
)


# indexエンドポイントを作成しindex.htmlを返す
@communication.route('/')
def index():
    return render_template('/index.html')


# ブログ投稿
@communication.route("/blog", methods=["GET","POST"])
def CPostBlog():
    form = BlogForm()

    # POSTの場合はフォームから送信された値を取得する
    if form.validate_on_submit():
        title = request.form.get('title')
        body = request.form.get('body')

        # アップロードされた画像ファイルを取得する
        file = request.files['image']

        # ファイルのファイル名と拡張子を取得し、ファイル名をuuidに変換する
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        # 画像を保存する
        image_path = Path(current_app.config["UPLOAD_FOLDER"], image_uuid_file_name)
        file.save(image_path)

        # ブログを作成する
        blog = Blog(
            title=title, 
            body=body,
            image_path=image_uuid_file_name,
            user_id=current_user.id
        )

        # ブログを追加してコミットする
        db.session.add(blog)
        db.session.commit()

        # ブログ一覧画面へリダイレクトする
        return redirect(url_for('communication.blog'))

    blogs = db.session.query(Blog, User).join(User).filter(Blog.blog_activate == True).order_by(Blog.created_at.desc()).all()
    current_time = datetime.datetime.now()

    return render_template("/blog.html", form=form, blogs=blogs, current_time=current_time)


# 新着ブログ一覧エンドポイントを作成する
@communication.route('/blog')
def blog():
    # ブログモデルとユーザーモデルを結合し、Blogのblog_activateがTrueのものを逆順で取得する
    blogs = db.session.query(Blog, User).join(User).filter(Blog.blog_activate == True).order_by(Blog.created_at.desc()).all()

    return render_template('/blog.html', blogs=blogs)


# ブログ詳細エンドポイントを作成する
@communication.route('/blog/<blog_id>')
def blog_detail(blog_id):
    # ブログモデルとユーザーモデルを結合し、Blogのidが一致するものを取得する
    blog = db.session.query(Blog, User).join(User).filter(Blog.id == blog_id).first()

    return render_template('/blog_detail.html', blog=blog)


# 他ユーザーのマイページエンドポイントを作成する
@communication.route('/other/<user_id>')
def other(user_id):
    # ユーザーモデルを取得する
    other = User.query.filter_by(id=user_id).first()
    form = FollowForm()
    # ブログモデルとユーザーモデルを結合し、Blogのuser_idが一致するものを逆順で取得する
    blogs = db.session.query(Blog, User).join(User).filter(Blog.user_id == user_id).order_by(Blog.created_at.desc()).all()

    # もしログインしているならば
    if current_user.is_authenticated:
        # ユーザーのFollowモデルを取得する
        follow = Follow.query.filter_by(follower_id=current_user.id, followee_id=other.id).first()
        # ログインしているユーザーのidと、otherのidが一致するならば、自分のマイページを表示する
        if current_user.id == other.id:
            return redirect(url_for('mypage.profile', user_id=other.id))
        # もしログインしているユーザーがotherをフォローしているならば、
        elif follow:
            # フォローボタンの,valueをフォローを解除するにし、formタグのactionをunfollowにする
            form.submit.label.text = 'フォローを解除する'
            form.submit.render_kw = {'class': 'btn btn-danger'}
            form.submit.render_kw = {'formaction': url_for('communication.unfollow', user_id=other.id)}
            return render_template('/other.html', other=other, form=form, blogs=blogs)
        # そうでないならば(ログインユーザーがotherをフォローしていないなら)、フォローボタンを表示する
        else:
            return render_template('/other.html', other=other, form=form, blogs=blogs)
    # ログインしていないならば、otherのマイページを表示する
    else:
        return render_template('/other.html', other=other, blogs=blogs, form=form)


# フォローするエンドポイントを作成する
@communication.route('/follow/<user_id>', methods=['POST'])
@login_required
def follow(user_id):
    # フォローするユーザーを取得する
    followee = User.query.filter_by(id=user_id).first()
    # フォローするユーザーのidと、ログインしているユーザーのidが一致するならば、マイページを表示する
    if current_user.id == followee.id:
        return redirect(url_for('mypage.profile', user_id=followee.id))

    # そうでないならば、フォローするユーザーをフォローする
    else:
        # フォローするユーザーをフォローする
        follow = Follow(follower_id=current_user.id, followee_id=followee.id)
        db.session.add(follow)
        db.session.commit()
        return redirect(url_for('communication.other', user_id=followee.id))


# フォロー解除するエンドポイントを作成する
@communication.route('/unfollow/<user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    # フォロー解除するユーザーを取得する
    followee = User.query.filter_by(id=user_id).first()
    # フォロー解除するユーザーのidと、ログインしているユーザーのidが一致するならば、マイページを表示する
    if current_user.id == followee.id:
        return redirect(url_for('mypage.profile', user_id=followee.id))

    # そうでないならば、フォロー解除するユーザーをフォロー解除する
    else:
        # フォロー解除するユーザーをフォロー解除する
        follow = Follow.query.filter_by(follower_id=current_user.id, followee_id=followee.id).first()
        db.session.delete(follow)
        db.session.commit()
        return redirect(url_for('communication.other', user_id=followee.id))


# 掲示板のメイン画面を作成する
@communication.route('/board')
def board():
    # 掲示板モデルとユーザーモデルを結合し、Boardのboard_activateがTrueのものを逆順で取得する
    boards = db.session.query(Board, User).join(User).filter(Board.board_activate == True).order_by(Board.created_at.desc()).all()
    form = BoardForm()

    # もしログインしているならば
    if current_user.is_authenticated:
        # レンダリング
        return render_template('/board.html', boards=boards, form=form)
    # ログインしていないならば、
    else:
        # 投稿ボタンをdisabledにし、ログインしてくださいと表示する
        form.submit.render_kw = {'disabled': 'disabled'}
        form.submit.label.text = '投稿にはログインが必要です'
        # レンダリング
        return render_template('/board.html', boards=boards, form=form)


# 掲示板の投稿エンドポイントを作成する
@communication.route('/board/create', methods=['POST'])
@login_required
def create_board():
    # フォームから入力された値を取得する
    form = BoardForm()
    title = form.title.data
    body = form.body.data
    # 掲示板を作成する
    board = Board(user_id=current_user.id, title=title, body=body)
    db.session.add(board)
    db.session.commit()
    return redirect(url_for('communication.board'))



# 掲示板の詳細画面を作成する
@communication.route('/board/<int:board_id>')
def board_detail(board_id):
    # 掲示板モデルとユーザーモデルを結合し、Boardのidが一致するものを取得する
    board = db.session.query(Board, User).join(User).filter(Board.id == board_id).first()
    # コメントフォームを作成する
    form = CommentForm()

    # コメントモデルとユーザーモデルを結合し、Commentのboard_idが一致するものを投稿日時の降順で取得する
    comments = db.session.query(Comment, User).join(User).filter(Comment.board_id == board_id).order_by(Comment.created_at.desc()).all()
    current_time = datetime.datetime.now()

    # もしログインしているならば
    if current_user.is_authenticated:
        # レンダリング
        return render_template('/board_detail.html', board=board, form=form, comments=comments, current_time=current_time)
    # ログインしていないならば、
    else:
        # コメントボタンをdisabledにし、ログインしてくださいと表示する
        form.submit.render_kw = {'disabled': 'disabled'}
        form.submit.label.text = 'コメントにはログインが必要です'
        # レンダリング
        return render_template('/board_detail.html', board=board, form=form, comments=comments, current_time=current_time)



# コメントするエンドポイントを作成する
@communication.route('/comment/<int:board_id>', methods=['POST'])
@login_required
def comment(board_id):
    form = CommentForm(request.form)  # フォームをリクエストのデータで初期化する
    if form.validate_on_submit():  # バリデーションをトリガーする
        body = form.body.data
        comment = Comment(board_id=board_id, user_id=current_user.id, body=body)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('communication.board_detail', board_id=board_id))




# ユーザーチャットのトップページ（ユーザーリストページ）を作成する
@communication.route('/Chat_List')
@login_required
def Chat_List():
    # current_userがフォローしているユーザーとcurrent_userをフォローしているユーザーを取得する
    followees = Follow.query.filter_by(follower_id=current_user.id).all()
    followers = Follow.query.filter_by(followee_id=current_user.id).all()
    # チャット相手のユーザーを格納するリストを作成する
    users = []
    # current_userがフォローしているユーザーをusersに格納する
    for followee in followees:
        users.append(User.query.filter_by(id=followee.followee_id).first())
    # current_userをフォローしているユーザーをusersに格納する
    for follower in followers:
        users.append(User.query.filter_by(id=follower.follower_id).first())
    # usersを重複なしにする
    users = list(set(users))
    # レンダリング
    return render_template('/Chat_List.html', users=users)



# チャット機能（本体）の実装
@communication.route('/Chat_User/<int:user_id>', methods=['GET', 'POST'])
@login_required
def Chat_User(user_id):
    chat_user = User.query.get_or_404(user_id)
    chat_messages = Chat.query.filter(
        ((Chat.sender_id == current_user.id) & (Chat.receiver_id == user_id)) |
        ((Chat.sender_id == user_id) & (Chat.receiver_id == current_user.id))
    ).order_by(Chat.created_at).all()

    # フォームのインスタンス化
    form = ChatForm()

    if form.validate_on_submit():
        message_body = form.message_body.data
        new_chat = Chat(sender_id=current_user.id, receiver_id=user_id, body=message_body)
        db.session.add(new_chat)
        db.session.commit()

        return redirect(url_for('communication.Chat_User', user_id=user_id))

    return render_template('/Chat_User.html', chat_user=chat_user, chat_messages=chat_messages, form=form)



