from pymongo import MongoClient
import os
from dotenv import load_dotenv  # avoid hardcoding passwords

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

# handle connection pooling
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# collections
industries_collection = db["industries"]
articles_collection = db["articles"]
insights_collection = db["insights"]
