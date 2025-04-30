from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from resources.auth import auth_bp
from models import db
from flask_cors import CORS
from flask import send_from_directory
from resources.books import book_bp

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # or your preferred database
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # replace with a strong secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # token expiration in seconds
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(book_bp, url_prefix='/api')

CORS(app)
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
