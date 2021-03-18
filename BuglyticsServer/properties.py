import os
import psycopg2
import traceback
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()
    print("Environment Loaded from .env file")
else:
    print("Environment Variables will be used directly from environment.")

postgres_url = os.getenv("POSTGRESURL")
secret_key = os.getenv("SECRET")

__PG_CONNECTION__ = None
try:
    __PG_CONNECTION__ = psycopg2.connect(postgres_url)
    print("Connected to Database Successfully")
except Exception as e:
    traceback.print_exc()
    print("Error Connecting Database")

# Getter Methods
def get_db_instance():
    return __PG_CONNECTION__

def get_site_secret_key():
    return secret_key