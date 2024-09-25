from flask import Blueprint, request, jsonify
from config.db import db
from sqlalchemy import Enum, DECIMAL
from datetime import datetime
from ..auth.auth0 import requires_auth
from ..models import Cart, Offer
# from flask_jwt_extended import jwt_required, get_jwt_identity


cart_bp = Blueprint('cart', __name__)

# @cart_bp.post('/cart/add')
# @requires_auth
# def add_cart(payload):
#     user_id = payload['sub']  # Extraire le user_id du JWT
#     data = request.get_json()
#     total_price = data.get("total_price")
#     status = data.get("status", 'Pending')

#     # Crée une nouvelle instance de Cart
#     new_cart = Cart(
#         user_id=user_id,
#         total_price=total_price,
#         status=status
#     )

#     db.session.add(new_cart)
#     db.session.commit()

#     return {"id": new_cart.id, "message": f"Cart with status {status} created, price: {total_price}"}, 201



# <int:item_id>
@cart_bp.post('/add-to-cart/<int:item_id>')
@requires_auth
def add_to_cart(payload, item_id):
    # return {"message": f"Received : {item_id}", "id": f"{payload['sub']}" }
    # print(f"Received payload: {payload['sub']}")

    current_user_id = payload['sub'] 
    item_to_add = Offer.query.get(item_id)
    item_exists = Cart.query.filter_by(offer_link=item_id, user_link=current_user_id).first()

    if item_exists:
        try:
            item_exists.quantity = item_exists.quantity +1
            db.session.commit()
            return {"message": f"quantity of { item_exists.offer.name } has been updated"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"quantity of { item_exists.offer.name } not updated"}, 500
        
    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.offer_link = item_to_add.id
    new_cart_item.user_link = current_user_id

    try:
        db.session.add(new_cart_item)
        db.session.commit()

        return {"message": f"${item_to_add.name} added to cart"}, 201
    except Exception as e:
        db.session.rollback()
        return {"message": f"{item_to_add.name} has not been added to cart"}


@cart_bp.get('/cart')
@requires_auth
def show_cart(payload):
    current_user_id = payload['sub'] 
    cart = Cart.query.filter_by(user_link=current_user_id).all()

    amount = 0
    cart_items = []
    
    # Parcourir les articles du panier pour calculer le montant total et collecter les détails
    for item in cart:
        item_data = {
            "offer_id": item.offer.id,
            "offer_name": item.offer.name,
            "price": item.offer.price,
            "quantity": item.quantity,
            "subtotal": item.offer.price * item.quantity
        }
        cart_items.append(item_data)
        amount += item_data["subtotal"]
    
    # Retourner les articles et le montant total du panier
    return {
        "cart_items": cart_items,
        "total_amount": amount
    }, 200


@cart_bp.get('/pluscart')
@requires_auth
def plus_cart(payload):
    current_user_id = payload['sub'] 
    cart_id = request.args.get('id')
    cart_item = Cart.query.get(cart_id)
    cart_item.quantity = cart_item.quantity +1
    db.session.commit()

    cart = Cart.query.filter_by(user_link=current_user_id).all()

    amount = 0
    cart_items = []

    # Parcourir le panier pour calculer le montant total et collecter les détails des articles
    for item in cart:
        item_data = {
            "offer_id": item.offer.id,
            "offer_name": item.offer.name,
            "price": item.offer.price,
            "quantity": item.quantity,
            "subtotal": item.offer.price * item.quantity
        }
        cart_items.append(item_data)
        amount += item_data["subtotal"]

    # Préparer les données de l'article mis à jour
    updated_item_data = {
        "offer_id": item.offer.id,
        "offer_name": cart_item.offer.name,
        "price": cart_item.offer.price,
        "quantity": cart_item.quantity,
        "subtotal": cart_item.offer.price * cart_item.quantity
    }

    # Retourner les détails de l'article mis à jour et le montant total du panier
    data = {
        "updated_item": updated_item_data,
    }

    return jsonify(data), 200


@cart_bp.get('/minuscart')
@requires_auth
def minus_cart(payload):
    current_user_id = payload['sub'] 
    cart_id = request.args.get('id')
    # cart_item = Cart.query.get(cart_id)
    # cart_item.quantity = cart_item.quantity -1

    # Vérification que l'ID de l'article est fourni
    if not cart_id:
        return jsonify({"error": "L'ID de l'article est manquant"}), 400

    # Vérification que l'article existe dans la base de données
    cart_item = Cart.query.get(cart_id)
    if not cart_item:
        return jsonify({"error": "L'article avec cet ID n'existe pas"}), 404

    # Vérification que l'article appartient bien à l'utilisateur connecté
    if cart_item.user_link != current_user_id:
        return jsonify({"error": "Cet article ne vous appartient pas"}), 403

    # Empêcher la quantité de descendre en dessous de 1
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        return jsonify({"error": "Impossible de réduire la quantité en dessous de 1"}), 400

    db.session.commit()

    cart = Cart.query.filter_by(user_link=current_user_id).all()

    amount = 0
    cart_items = []

    # Parcourir le panier pour calculer le montant total et collecter les détails des articles
    for item in cart:
        item_data = {
            "offer_name": item.offer.name,
            "price": item.offer.price,
            "quantity": item.quantity,
            "subtotal": item.offer.price * item.quantity
        }
        cart_items.append(item_data)
        amount += item_data["subtotal"]

    # Préparer les données de l'article mis à jour
    updated_item_data = {
        "offer_name": cart_item.offer.name,
        "price": cart_item.offer.price,
        "quantity": cart_item.quantity,
        "subtotal": cart_item.offer.price * cart_item.quantity
    }

    # Retourner les détails de l'article mis à jour et le montant total du panier
    data = {
        "updated_item": updated_item_data,
    }

    return jsonify(data), 200



@cart_bp.get('/removecart')
@requires_auth
def remove_cart(payload):
    current_user_id = payload['sub'] 
    cart_id = request.args.get('id')
    cart_item = Cart.query.get(cart_id)
    db.session.delete(cart_item)
    db.session.commit()

    cart = Cart.query.filter_by(user_link=current_user_id).all()

    amount = 0
    cart_items = []
    
    # Parcourir les articles du panier pour calculer le montant total et collecter les détails
    for item in cart:
        item_data = {
            "offer_name": item.offer.name,
            "price": item.offer.price,
            "quantity": item.quantity,
            "subtotal": item.offer.price * item.quantity
        }
        cart_items.append(item_data)
        amount += item_data["subtotal"]
    
    # Retourner les articles et le montant total du panier
    return {
        "cart_items": cart_items,
        "total_amount": amount
    }, 200