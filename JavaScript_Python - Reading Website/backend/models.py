from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_author = db.Column(db.Boolean, default=False)  # New field to check if user is an author
    #books = db.relationship('Book', backref='author', lazy=True)
    
    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')
    
    @staticmethod
    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    origin_book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    branch_info = db.Column(db.String(200), nullable=True)

    origin_book = db.relationship('Book', remote_side=[id], backref='branches')

class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True,nullable=False)

    # Relationships
    book = db.relationship('Book', backref=db.backref('chapters', lazy=True))
    
class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    books = db.relationship('Book', backref='author', lazy=True)


class ReadingList(db.Model):
    __tablename__ = 'reading_list'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)


class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

class BranchRequest(db.Model):
    __tablename__ = 'branch_requests'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    request_summary = db.Column(db.Text, nullable=True)
    request_info = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, created

    book = db.relationship('Book', backref='branch_requests', lazy=True)
    requester = db.relationship('User', backref='sent_branch_requests', lazy=True)
