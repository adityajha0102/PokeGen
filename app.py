from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd

from src.image_generation import get_Image
from src.stats_generation import hp_stats, minmax_stats, get_info
from src.process_data import process_dataset
from src.battle_generation import get_battle_details
from src.top_list import top_pokemon

from helpers.validate import validate_base_parameter, validate_special_parameter
from helpers.llm_utils import llm
from helpers.db_connect import connect_db
from helpers.db_upload import upload_data, delete_all_files
from helpers.db_search import search_files
from helpers.errors import AppError, ValidationError, NotFoundError

load_dotenv()
app = Flask(__name__)
CORS(app)

@app.errorhandler(AppError)
def handle_app_error(error):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response
    
@app.route('/generate_pokemon', methods=['POST'])
def generate():
    try:
        try:
            data = request.get_json()
            user_prompt = data.get("user_prompt", "")
            base_hp = validate_base_parameter(user_prompt.get("base_hp"), "Base HP", 10, 99)
            base_speed = validate_base_parameter(user_prompt.get("base_speed"), "Base Speed", 10, 99)
            base_defense = validate_base_parameter(user_prompt.get("base_defense"), "Base Defense", 10, 89)
            base_attack = validate_base_parameter(user_prompt.get("base_attack"), "Base Attack", 10, 89)
            base_special_defense = validate_base_parameter(user_prompt.get("base_special_defense"), "Base Special Defense", 10, 99)
            base_special_attack = validate_base_parameter(user_prompt.get("base_special_attack"), "Base Special Attack", 10, 99)
            
        except AttributeError as ae:
            # Handle attribute errors (e.g., if request.get_json() fails)
            raise ValidationError('Invalid JSON format in request')
        
        base_special_defense = validate_special_parameter(base_special_defense, "Base Special Defense", base_defense, "Base Defense")
        base_special_attack = validate_special_parameter(base_special_attack, "Base Special Attack", base_attack, "Base Attack")

        img_data = get_Image(user_prompt)
        name, pokemon_type, height, weight, abilities, back_story = get_info(llm, user_prompt)
        min_hp, max_hp = hp_stats(base_hp)
        min_defense, max_defense = minmax_stats(base_defense)
        min_attack, max_attack = minmax_stats(base_attack)
        min_special_defense, max_special_defense = minmax_stats(base_special_defense)
        min_special_attack, max_special_attack = minmax_stats(base_special_attack)
        min_speed, max_speed = minmax_stats(base_speed)
                    
        json_data = {
            'Pokemon': name,
            'Type': pokemon_type,
            'Height': height,
            'Weight': weight,
            'Abilites': abilities,
            'Backstory': back_story,
            'HP Min': min_hp,
            'HP Base': base_hp,
            'HP Max': max_hp,
            'Defense Min': min_defense,
            'Defense Base': base_defense,
            'Defense Max': max_defense,
            'Min Attack': min_attack,
            'Base Attack': base_attack,
            'Max Attack': max_attack,
            'Min Special Defense': min_special_defense,
            'Base Special Defense': base_special_defense,
            'Max Special Defense': max_special_defense,
            'Min Special Attack': min_special_attack,
            'Base Special Attack': base_special_attack,
            'Max Special Attack': max_special_attack,
            'Min Speed': min_speed,
            'Base Speed': base_speed,
            'Max Speed': max_speed,
            'Simplified Type': pokemon_type,
            'Image Data': img_data
        }

        return jsonify(json_data)
    
    except AppError as e:
        return jsonify({'error': e.message}), e.status_code

    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/upload_db', methods=['POST'])
def upload():
    processed_df = process_dataset(r"D:\\Projects\\PokeGen\\data\\pokemonDB_dataset.csv")
    db, fs = connect_db()
    return upload_data(fs, processed_df)
    

@app.route('/delete_all', methods=['POST'])
def delete_all():
    db, fs = connect_db()
    return delete_all_files(db, fs)

@app.route('/db_search', methods=['POST'])
def search():
    data = request.get_json()
    query_fields = dict(data.get("query", ""))
    last_id = data.get("last_id", "")
    db, fs = connect_db()
    return jsonify(search_files(db, fs, query_fields, last_id=last_id))    

@app.route('/battle_simulate', methods=['POST'])
def battle_simulate():
    try:
        data = request.get_json()
        pokemon1 = dict(data.get("Pokemon1", ""))
        pokemon2 = dict(data.get("Pokemon2", ""))
        winner, result = get_battle_details(pokemon1, pokemon2)
        result['Winner'] = winner['Pokemon']
        return jsonify(result) 
    except:
        return jsonify({'error': "Something went wrong"}), 404
    
@app.route('/top_count', methods=['POST'])
def top_count():
    query = dict()
    db, fs = connect_db()
    pokemon_all = search_files(db, fs, query, check='top')
    pokemon_all_list = []
    for i in pokemon_all:
        i['metadata']['_id'] = i['_id']
        pokemon_all_list.append(i['metadata'])
    return top_pokemon(pokemon_all_list)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)