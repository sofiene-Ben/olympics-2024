from flask import Blueprint, jsonify
from ..auth.auth0 import requires_auth
from ..auth.role import requires_role


admin_bp = Blueprint('role', __name__)

@admin_bp.get('/admin/dashboard')
# @requires_auth  # Décorateur pour vérifier l'authentification
@requires_role('admin')  # Décorateur pour vérifier le rôle d'administrateur
def admin_dashboard(payload):
    return jsonify({"message": "Welcome to the admin dashboard!"})
