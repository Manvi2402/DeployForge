from pymongo import MongoClient

# connect to MongoDB
client = MongoClient("mongodb://localhost:27017")

# database
db = client["deployforge"]

# collection
deployments_collection = db["deployments"]