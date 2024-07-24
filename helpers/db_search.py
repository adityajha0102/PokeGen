from flask import jsonify

def search_files(db, fs, query_fields, check = 'specific'):
    try:
        # Construct the query dynamically
        query = {}
        for key, value in query_fields.items():
            if value:  # Exclude empty or None values
                query[key] = value
        
        # Perform the search in fs.files collection
        cursor = db.fs.files.find(query)

        # Convert cursor to list to retrieve all matching documents
        results = []
        for document in cursor:
            # Convert ObjectId to string for JSON serialization
            document['_id'] = str(document['_id'])
            results.append(document)
        if check == 'top':
            return results
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': f"Error searching files in Database: {e}"}), 500
        
