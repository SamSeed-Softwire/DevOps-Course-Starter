"""Flask configuration class."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you forget to run setup.sh?")
