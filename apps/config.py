from pathlib import Path

basedir = Path(__file__).parent.parent


# BaseConfigクラスを作成する
class BaseConfig:
    SECRET_KEY = "secret_key"
    WTF_CSRF_SECRET_KEY = "secret_key"
    # 画像アップロード先にapps/imagesを指定する
    UPLOAD_FOLDER = str(Path(basedir, "apps", "images"))
    # 動画アップロード先にapps/moviesを指定する
    MOVIE_FOLDER = str(Path(basedir, "apps", "movies"))


# BaseConfigクラスを継承してLocalConfigクラスを作成する
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


# config辞書にマッピングする
config = {
    "local": LocalConfig,
}
