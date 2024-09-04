# import os
# import psycopg2
# from dotenv import load_dotenv
# from flask import Flask

# load_dotenv()

# def create_app():
#     app = Flask(__name__)

#     url = os.getenv("DATABASE_URL")

#     try:
#         app.connexion = psycopg2.connect(url)  # Attribue la connexion à l'objet app
#     except psycopg2.OperationalError as e:
#         print(f"Unable to connect to the database: {e}")
#         app.connexion = None

#     # Importation et enregistrement des Blueprints
#     from .routes.offer import offer_bp
#     app.register_blueprint(offer_bp, url_prefix='/api')

    # @app.teardown_appcontext
    # def close_connexion(exception):
    #     if app.connexion is not None:
    #         app.connexion.close()

    # return app

import os
from flask import Flask
from config.db import db  # Assurez-vous que le chemin est correct
from dotenv import load_dotenv
from flask_migrate import Migrate
from .routes.offer import offer_bp

load_dotenv()

app = Flask(__name__)

# Configuration de l'application
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db.init_app(app)

# Initialisation de Flask-Migrate
migrate = Migrate(app, db)

# Enregistrement du Blueprint
app.register_blueprint(offer_bp)

@app.teardown_appcontext
def teardown_db(exception):
    db.session.remove()





