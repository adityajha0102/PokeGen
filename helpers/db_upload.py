import os
import io
from flask import jsonify

def upload_data(fs, df):
    try:
        # Iterate through the dataframe and store images and metadata
        for index, row in df.iterrows():
            image_path = row['image_path']
            metadata = row.drop(labels='image_path').to_dict()
            
            # Open and read the image file, and convert it to BytesIO
            with open(image_path, 'rb') as f:
                image_data = io.BytesIO(f.read())
            
            # Store the image in GridFS with metadata
            file_id = fs.put(image_data, filename=os.path.basename(image_path), metadata=metadata)
            
        return jsonify({"message":"Images and metadata have been stored successfully."}), 200
    except:
        return jsonify({'error': "Images and metadata couldn't be stored. Try again later"}), 500
    

def delete_all_files(db, fs):
    try:
        # Delete all documents from fs.files collection
        db.fs.files.delete_many({})
        # Delete all documents from fs.chunks collection
        db.fs.chunks.delete_many({})
        return jsonify({'message': 'All data deleted from GridFS.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
