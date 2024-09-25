import sys
import os

# Ajoute le répertoire racine de ton projet au sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from olympics_back.app.offer.models_offer import Pffer
print("Import successful!")
