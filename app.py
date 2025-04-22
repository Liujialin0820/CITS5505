from flask import Flask, render_template
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
from config import Config
from exts import db, migrate
from flask_wtf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)

    from apps.cms import models
    from apps.front import models
    from apps.common import models
    db.init_app(app)
    migrate.init_app(app, db)
    CSRFProtect(app)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=8000)
