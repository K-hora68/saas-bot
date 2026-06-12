from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
# Allow the frontend to send Authorization header and JSON content-type
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}},
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True)

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Flask app is running well"


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Username, email, and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    if not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid password"}), 401
    
    access_token = create_access_token(identity=user.user_id)
    return jsonify({
        "access_token": access_token,
        "user_id": user.user_id,
        "username": user.username
    })


@app.route('/is_authenticated', methods=['GET'])
@jwt_required()
def is_authenticated():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email
    }), 200

if __name__ == '__main__':
    app.run(debug=True)