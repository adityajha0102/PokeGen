from flask import jsonify

def search_files(db, fs, query_fields):
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
        print(len(results))
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': f"Error searching files in Database: {e}"}), 500
        
'''if __name__=="__main__":
    # Example search query (modify as per your requirement)
    query_fields = {
        "metadata.Simplified Type": "Fire",
        # Add more fields as needed
    }
    results = search_files(query_fields)

    # Process the results as needed
    print(f"Found {len(results)} files matching the query.")

    print(results)'''