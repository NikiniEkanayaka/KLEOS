import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

# -------------------------
# LOG DIRECTORY & FILE
# -------------------------
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

CURRENT_TIME_STAMP = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
log_file_path = os.path.join(LOG_DIR, f"log_{CURRENT_TIME_STAMP}.log")

# -------------------------
# LOGGER SETUP
# -------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # captures all levels

# File handler
file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
