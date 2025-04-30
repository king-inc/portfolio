# book.py
import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from models import db, Book, User, Chapter, BranchRequest
from flask_jwt_extended import jwt_required, get_jwt_identity

UPLOAD_FOLDER = 'uploads'
CHAPTER_FOLDER = 'chapters'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

book_bp = Blueprint('book', __name__)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@book_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_data = [{"id": book.id, "title": book.title, "content": book.content, "author_id": book.author_id, "image": book.image} for book in books]
    return jsonify(books_data), 200

@book_bp.route('/my-books', methods=['GET'])
@jwt_required()
def get_my_books():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user.is_author:
        return jsonify({"msg": "User is not an author"}), 403
    
    books = Book.query.filter_by(author_id=user_id).all()
    books_data = [{"id": book.id, "title": book.title, "content": book.content, "image": book.image} for book in books]
    return jsonify(books_data), 200

@book_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = User.query.get(book.author_id)

    # Format the response data
    book_data = {
        "id": book.id,
        "title": book.title,
        "content": book.content,
        "image_filename": book.image,
        "author": {
            "id": author.id,
            "username": author.username}
    }
    return jsonify(book_data), 200

@book_bp.route('/create-book', methods=['POST'])
@jwt_required()
def create_book():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.is_author:
        return jsonify({"msg": "Only authors can create books"}), 403

    data = request.form
    title = data.get('title')
    content = data.get('content')
    req_id = int(data.get('req_id'))
    origin_book_id = int(data.get('origin_book_id'))
    branch_info = data.get('branch_info')

    # Handle the image file if uploaded
    file = request.files.get('image')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
    else:
        return jsonify({"msg": "You need to upload an image"}), 403
    
    if origin_book_id > 0:
        req = BranchRequest.query.get_or_404(req_id)
        new_book = Book(title=title, content=content, image=filename, author_id=user_id, origin_book_id=origin_book_id, branch_info=branch_info)
        req.status = "created"
    else:
        new_book = Book(title=title, content=content, image=filename, author_id=user_id, origin_book_id=origin_book_id)
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({"msg": "Book created successfully"}), 201


@book_bp.route('/books/<int:book_id>/chapter/<int:chapter_id>', methods=['POST'])
@jwt_required()
def add_chapter(book_id,chapter_id):
    user_id = get_jwt_identity()
    book = Book.query.get_or_404(book_id)
    chapter_data = Chapter.query.filter_by(id=chapter_id,book_id=book_id).first()
    
    # Verify the user is the author of the book
    if book.author_id != user_id:
        return jsonify({"msg": "Unauthorized access"}), 403
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    # Create and add new chapter
    if chapter_data:
        chapter_data.title = title
        f = open(chapter_data.content, "w")
        f.write(content)
        f.close()
    else:
        filename = os.path.join(CHAPTER_FOLDER,secure_filename("%s-%s-%s.txt" % (str(book_id),str(chapter_id),title)))
        f = open(filename, "w")
        f.write(content)
        f.close()
        new_chapter = Chapter(id=chapter_id, title=title, content=filename, book_id=book_id)
        db.session.add(new_chapter)
    db.session.commit()
    
    return jsonify({"msg": "Chapter added successfully"}), 201

@book_bp.route('/books/<int:book_id>/chapters', methods=['GET'])
def get_chapters(book_id):
    chapters = Chapter.query.filter_by(book_id=book_id).all()

    chapters_data = [
        {"id": chapter.id, "title": chapter.title, "content": chapter.content}
        for chapter in chapters
    ]
    
    return jsonify({"chapters": chapters_data}), 200

@book_bp.route('/books/<int:book_id>/chapter/<int:chapter_id>', methods=['GET'])
def get_book_chapter(book_id,chapter_id):
    book = Book.query.get_or_404(book_id)
    chapter = Chapter.query.filter_by(book_id=book_id,id=chapter_id).first()

    if chapter:
        content = open(chapter.content, "r")
        # Format the response data
        chapter_data = {
            "id": chapter.id,
            "title": chapter.title,
            "content": content.read()
        }
        content.close()
    else:
        chapter_data = {
            "id": chapter_id,
            "title": "",
            "content": ""
        }
    return jsonify(chapter_data), 200

@book_bp.route('/books/<int:book_id>/branch-request', methods=['POST'])
@jwt_required()
def request_branch(book_id):
    user_id = get_jwt_identity()
    book = Book.query.get_or_404(book_id)

    data = request.get_json()
    request_summary = data.get('request_summary')
    request_info = data.get('request_info')

    if book.author_id == user_id:
        return jsonify({"msg": "You cannot request to branch your own book"}), 400

    existing_request = BranchRequest.query.filter_by(book_id=book_id, requester_id=user_id, status='pending').first()
    if existing_request:
        return jsonify({"msg": "You have already requested to branch this book"}), 400

    branch_request = BranchRequest(book_id=book_id, requester_id=user_id, request_summary=request_summary, request_info=request_info)
    db.session.add(branch_request)
    db.session.commit()

    return jsonify({"msg": "Branch request submitted"}), 201


@book_bp.route('/my-books/branch-requests', methods=['GET'])
@jwt_required()
def get_all_branch_requests():
    user_id = get_jwt_identity()
    own_requests = BranchRequest.query.filter(BranchRequest.requester_id == user_id, BranchRequest.status != 'created').all()
    author_requests = BranchRequest.query.join(Book).filter(Book.author_id == user_id, BranchRequest.status == 'pending').all()

    own = [{"id": req.id, "book_title":req.book.title, "request_info": req.request_info, "status": req.status} for req in own_requests]
    author = [{"id": req.id, "book_title":req.book.title, "requester": req.requester.username, "request_summary": req.request_summary, "request_info": req.request_info} for req in author_requests]
    
    return jsonify({"own": own, "author": author}), 200

@book_bp.route('/my-books/branch-requests/<int:request_id>', methods=['GET'])
@jwt_required()
def get_specific_branch_request(request_id):
    user_id = get_jwt_identity()
    req = BranchRequest.query.get_or_404(request_id)

    if req.requester_id != user_id or req.status != "accepted":
        return jsonify({"msg": "Unauthorized"}), 403
    
    return jsonify({
        "title": (req.book.title+" branched"),
        "request_summary": req.request_summary,
        "request_info": req.request_info,
        "origin_id": req.book_id
    }), 200


@book_bp.route('/branch-requests/<int:request_id>', methods=['PATCH'])
@jwt_required()
def handle_branch_request(request_id):
    user_id = get_jwt_identity()
    branch_request = BranchRequest.query.get_or_404(request_id)

    if branch_request.book.author_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()
    status = data.get('status')
    if status not in ['accepted', 'rejected']:
        return jsonify({"msg": "Invalid status"}), 400

    branch_request.status = status
    db.session.commit()

    #if status == 'accepted':
    #    new_book = Book(title=f"{branch_request.book.title} (Branched)", author_id=branch_request.requester_id, origin_book_id=branch_request.book.id,)
    #    db.session.add(new_book)
    #    db.session.commit()
    #    return jsonify({"msg": "Branch request accepted and book created", "new_book_id": new_book.id}), 200

    return jsonify({"msg": "Branch request handled"}), 200
