import os
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI  = os.getenv("SQLALCHEMY_DATABASE_URI")