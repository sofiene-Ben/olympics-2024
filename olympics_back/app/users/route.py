from flask import Blueprint, request, jsonify
from app import db
from ..models import User
from ..auth.auth0 import requires_auth

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
@requires_auth
def create_user(payload, *args, **kwargs):
    # data = request.get_json()
    
    auth0_user_id = payload['sub']  
    # auth0_user_id = data.get('auth0_id')
    # email = data.get('email')

    # Vérifie si l'utilisateur existe déjà dans la base de données
    user = User.query.filter_by(auth0_user_id=auth0_user_id).first()

    if not user:
        # Crée un nouvel utilisateur s'il n'existe pas
        new_user = User(auth0_user_id=auth0_user_id)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Utilisateur cree avec succes"}), 201
    else:
        return jsonify({"message": "L'utilisateur existe deja"}), 200
