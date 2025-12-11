import os
import logging
from logging.handlers import RotatingFileHandler

# Chemins 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Créer les dossiers si non existants
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

#  Fichiers 
LOG_FILE = os.path.join(LOG_DIR, "app.log")
CSV_FILE = os.path.join(DATA_DIR, "ventes_2025.csv")

#  Logging 
def setup_logger(name: str = "projet-python-pmn"):
    """
    Configure le logger avec rotation de fichiers.
    DEBUG -> INFO -> WARNING -> ERROR
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Format du log
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Handler fichier avec rotation
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3,encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Ajouter handlers si pas déjà présent
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
 