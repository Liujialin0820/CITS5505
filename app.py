from flask import Flask, render_template

# Import blueprints for modular route handling
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp

# Import config, DB, migration tools, CSRF protection
from config import Config
from exts import db, migrate
from flask_wtf import CSRFProtect


def create_app():
    """
    Factory function to create and configure the Flask app.
    Returns:
    Flask app instance
    """
    app = Flask(__name__)
    
    # Load settings from config.py
    app.config.from_object(Config)

    # Register blueprints (modular route groups)
    app.register_blueprint(cms_bp)     # Admin panel
    app.register_blueprint(front_bp)   # User-facing pages
    app.register_blueprint(common_bp)  # Shared APIs or routes

    # Ensure model definitions are imported before using the DB
    from apps.cms import models
    from apps.front import models
    from apps.common import models

    # Initialize database and migration support
    db.init_app(app)
    migrate.init_app(app, db)

    # Enable CSRF protection for form security
    CSRFProtect(app)
    
    return app


if __name__ == "__main__":
    # Local development server launch
    app = create_app()
    app.run(port=5000)  # Default: http://localhost:5000
