# import os
# import psycopg2
# from dotenv import load_dotenv

# # Charger les variables d'environnement
# load_dotenv()

# def get_db_connection():
#     """Crée et renvoie une nouvelle connexion à la base de données."""
#     url = os.getenv("DATABASE_URL")
#     try:
#         connexion = psycopg2.connect(url)
#         return connexion
#     except psycopg2.OperationalError as e:
#         print(f"Unable to connect to the database: {e}")
#         return None

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()