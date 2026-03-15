from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["deployforge"]

deployments_collection = db["deployments"]