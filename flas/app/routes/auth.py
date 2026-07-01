from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.users import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing required fields'}), 400

        user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password'])
        )

        db.session.add(user)
        db.session.commit()
        return jsonify({'message':'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing email or password'}), 400

        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({"message":"Invalid email or password"}), 401
        if not check_password_hash(user.password, data['password']):
            return jsonify({"message":"Invalid email or password"}), 401
        
        token = create_access_token(identity=str(user.id))

        return jsonify({
            "access_token": token,
            "user_id": user.user_id,
            "username": user.username
        }), 200
    except Exception as e:
        return jsonify({'message': f'Login failed: {str(e)}'}), 500

@auth_bp.route('/is_authenticated', methods=['GET'])
@jwt_required()
def is_authenticated():
    current_user_id = int(get_jwt_identity())
    print("Jwt identity:", current_user_id)
    print("type: ",type(current_user_id))
    user = User.query.get(current_user_id)
    if user:
        return jsonify({"authenticated": True, "user_id": user.user_id}), 200
    else:
        return jsonify({"authenticated": False}), 401


@auth_bp.route('/api/services', methods = ["POST"])
@jwt_required()
def create_service():
    user_id = get_jwt_identity()

    data = request.get_json()
    Services = data["Services"]

    for service in Services:
        new_service = Services(
            user_id = user_id,
            name = service["name"],
            decription = service["description"],
            price = service["price"]
        )
        db.session.add(new_service)
    db.session.commit()

    return jsonify({
        "message: ": "saved"
    })