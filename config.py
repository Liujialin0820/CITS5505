import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_location = "sqlite:///" + os.path.join(basedir, "app.db")


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or default_database_location
    SECRET_KEY = "amber_pearl_latte_is_the_best"

    CMS_USER_ID = "cmsuserid"
    FRONT_USER_ID = "frontuserid"
    FRONT_USER_INFO = "fdjsain"
