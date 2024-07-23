from pymongo import MongoClient
from gridfs import GridFS

def connect_db():
    mongo_uri = "mongodb+srv://adityajha0102:SMFZVF2RaiV5KHWo@pokegen-main.dvlerap.mongodb.net/?retryWrites=true&w=majority&appName=PokeGen-Main"

    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client.get_database('PokeGen-Main')

    # Set up GridFS
    fs = GridFS(db)
    return db, fs
