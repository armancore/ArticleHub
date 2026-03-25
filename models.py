from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize database
db = SQLAlchemy()

# User Model - Stores user information
class User(UserMixin, db.Model):
    """
    User model for storing user account information
    Inherits from UserMixin for Flask-Login functionality
    """
    # Primary key - unique identifier for each user
    id = db.Column(db.Integer, primary_key=True)
    
    # User credentials and info
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, default='No bio yet.')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Admin flag - set to True for admin users
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationships
    # One user can have many posts
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    # One user can have many comments
    comments = db.relationship('Comment', backref='commenter', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


# Post Model - Stores blog posts
class Post(db.Model):
    """
    Post model for storing blog articles
    """
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Post content
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key - links post to user
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    # One post can have many comments
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.title}>'


# Comment Model - Stores comments on posts
class Comment(db.Model):
    """
    Comment model for storing user comments on posts
    """
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Comment content
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.id}>'