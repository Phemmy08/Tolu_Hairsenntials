from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()  # Database instance
bcrypt = Bcrypt()  # Password hashing

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(50), unique=True, nullable=False)  # Unique username
    password_hash = db.Column(db.String(128), nullable=False)  # Hashed password

    def set_password(self, password):  # Hash password before storing
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):  # Check if password matches
        return bcrypt.check_password_hash(self.password_hash, password)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Product name
    description = db.Column(db.String(255), nullable=False)  # Product description
    price = db.Column(db.Float, nullable=False)  # Product price
    stock = db.Column(db.Integer, nullable=False)  # Available stock