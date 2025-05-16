from flask import Flask
from exts import db  # ✅ 从 exts 引入，不能再自己创建新的 SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)

    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.secret_key = 'test'
    else:
        app.config.from_object('config.Config')

    db.init_app(app)  # ✅ 正确绑定 db

    from . import hooks
    from .views import bp
    app.register_blueprint(bp)

    return app
