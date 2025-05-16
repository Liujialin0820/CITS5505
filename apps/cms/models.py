from exts import db  # Import SQLAlchemy instance for database operations
from datetime import datetime  # Import to set default join time
from werkzeug.security import generate_password_hash, check_password_hash  # Import password hashing utilities

class CMSUser(db.Model):
    __tablename__ = 'cms_user'  # Table name in the database

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key, auto-incremented
    username = db.Column(db.String(50), nullable=False)  # Admin user's username
    _password = db.Column(db.String(100), nullable=False)  # Hashed password (stored privately)
    email = db.Column(db.String(50), nullable=False, unique=True)  # Unique email for login
    join_time = db.Column(db.DateTime, default=datetime.now)  # Time of account creation

    def __init__(self, username, password, email):
        # Custom constructor to allow setting raw password
        self.username = username
        self.password = password  # Will use the setter to hash
        self.email = email

    @property
    def password(self):
        # Getter for password (usually unused directly)
        return self._password

    @password.setter
    def password(self, raw_password):
        # Automatically hashes the raw password before storing
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        # Compares a raw password with the stored hashed one
        result = check_password_hash(self.password, raw_password)
        return result
