# import os
# from flask import Flask
# from config.db import db  # Assurez-vous que le chemin est correct
# from dotenv import load_dotenv
# from flask_migrate import Migrate
# from offer.route import offer_bp
# from cart.route import cart_bp

# load_dotenv()


# #     return app
# app = Flask(__name__)

# # Configuration de l'application
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialisation de la base de données
# db.init_app(app)

# # Initialisation de Flask-Migrate
# migrate = Migrate(app, db)

# # Enregistrement du Blueprint
# app.register_blueprint(offer_bp)
# app.register_blueprint(cart_bp)

# @app.teardown_appcontext
# def teardown_db(exception):
#     db.session.remove()

import os
from flask import Flask
from config.db import db
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration de l'application
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db.init_app(app)

# Initialisation de Flask-Migrate
migrate = Migrate(app, db)

# Enregistrement des Blueprints
from .offer.route import offer_bp
from .cart.route import cart_bp
from .users.route import user_bp
from .admin.route import admin_bp

app.register_blueprint(offer_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)


@app.teardown_appcontext
def teardown_db(exception):
    db.session.remove()






