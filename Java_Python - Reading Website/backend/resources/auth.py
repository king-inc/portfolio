from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    new_user = User(username=username, password=User.hash_password(password))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and User.check_password(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@auth_bp.route('/become-author', methods=['POST'])
@jwt_required()
def become_author():
    current_user_id = get_jwt_identity()
    print(current_user_id)
    user = User.query.get(current_user_id)
    
    if user.is_author:
        return jsonify({"msg": "User is already an author"}), 400
    
    user.is_author = True
    db.session.commit()
    
    return jsonify({"msg": "User is now an author"}), 200

@auth_bp.route('/is-author', methods=['GET'])
@jwt_required()
def is_author():
    current_user_id = get_jwt_identity()
    print("ID: ", current_user_id)
    user = User.query.get(current_user_id)
    
    return jsonify(user.is_author)