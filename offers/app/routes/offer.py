# from flask import Blueprint, request, jsonify
# from config.db import get_db_connection

# offer_bp = Blueprint('offer', __name__)

# CREATE_OFFERS_TABLE = (
#     "CREATE TABLE IF NOT EXISTS offer (id SERIAL PRIMARY KEY, name TEXT);"
# )
# INSERT_OFFERS_RETURN_ID = "INSERT INTO offer (name) VALUES (%s) RETURNING id;"
# SELECT_ALL_OFFERS = "SELECT * FROM offer;"

# @offer_bp.post('/api/add_offer')
# def create_offer():
#     connexion = get_db_connection()
#     if connexion is None:
#         return {"error": "Database connection is not established"}, 500

#     data = request.get_json()
#     name = data["name"]
#     try:
#         with connexion:
#             with connexion.cursor() as cursor:
#                 cursor.execute(CREATE_OFFERS_TABLE)
#                 cursor.execute(INSERT_OFFERS_RETURN_ID, (name,))
#                 offer_id = cursor.fetchone()[0]
#         return {"id": offer_id, "message": f"Offer {name} created"}, 201
#     except Exception as e:
#         return {"error": str(e)}, 500
#     finally:
#         connexion.close()

# @offer_bp.get('/api/get_offer')
# def get_offers():
#     connexion = get_db_connection()
#     if connexion is None:
#         return {"error": "Database connection is not established"}, 500

#     try:
#         with connexion:
#             with connexion.cursor() as cursor:
#                 cursor.execute(SELECT_ALL_OFFERS)
#                 offers = cursor.fetchall()
#                 offer_list = [{"id": row[0], "name": row[1]} for row in offers]
#         return jsonify(offer_list), 200
#     except Exception as e:
#         return {"error": str(e)}, 500
#     finally:
#         connexion.close()


from flask import Blueprint, request, jsonify
from config.db import db

offer_bp = Blueprint('offer', __name__)

class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    max_tickets = db.Column(db.Integer)
    price = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False)

@offer_bp.post('/api/add_offer')
def create_offer():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    max_tickets = data.get("max_tickets")
    price = data.get("price")

    new_offer = Offer(
            name=name,
            description=description,
            max_tickets=max_tickets,
            price=price
                      )
    db.session.add(new_offer)
    db.session.commit()

    return {"id": new_offer.id, "message": f"Offer {name} created"}, 201

@offer_bp.get('/api/get_offer')
def get_offer():
    offers = Offer.query.all()
    offer_list = [{

        "id": offer.id,
        "name": offer.name,
        "descriptionn": offer.description,
        "max_tickets": offer.max_tickets,
        "price": offer.price

        } for offer in offers]

    return jsonify(offer_list), 200

@offer_bp.patch('/api/update_offer/<int:offer_id>')
def update_offer(offer_id):
    data = request.get_json()

    offer = Offer.query.get(offer_id)

    if not offer:
        return jsonify({"message": "offer not found"}), 404
    # offer.name = data.get("name", offer.name)
    # offer.description = data.get("description", offer.description)
    # offer.max_tickets = data.get("max_tickets", offer.max_tickets)
    # offer.price = data.get("price", offer.price)
    if "name" in data:
        offer.name = data["name"]
    if "description" in data:
        offer.description = data["description"]
    if "max_tickets" in data:
        offer.max_tickets = data["max_tickets"]
    if "price" in data:
        offer.price = data["price"]

    db.session.commit()

    # db.session.commit()
    return jsonify({"id": offer.id, "message": "Offer updated successfully"}), 200