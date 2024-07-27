from flask import jsonify
from bson import ObjectId
import base64

def search_files(db, fs, query_fields, check = 'specific', last_id = ""):
    try:
        # Construct the query dynamically
        query = {}
        for key, value in query_fields.items():
            if value:  # Exclude empty or None values
                query[key] = value
        if check=="specific":
            # Perform the search in fs.files collection
            if last_id=="":
                cursor = db.fs.files.find(query).limit(20)
            else:
                cursor = db.fs.files.find({'_id': {'$gt': ObjectId(last_id)}}).limit(21)
        else:
            cursor = db.fs.files.find(query)
        # Convert cursor to list to retrieve all matching documents
        results = []
        for document in cursor:
            if check=="specific":
                # Convert ObjectId to string for JSON serialization
                document['image data'] = search_image(db, fs, document)
            document['_id'] = str(document['_id'])
            results.append(document)
        return results
        
    except Exception as e:
        return {'error': f"Error searching files in Database: {e}"}
        

def search_image(db, fs, document):
    image_data = db.fs.chunks.find({'files_id': document['_id']})
    return base64.b64encode(image_data[0]['data']).decode('utf-8')