import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "for-no-reason"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    UPLOADS_DEFAULT_DEST = "app/uploads"
    UPLOADED_PHOTOS_DEST = "app/uploads"
    UPLOADED_PHOTOS_ALLOW = ("png", "jpg", "jpeg", "gif")
