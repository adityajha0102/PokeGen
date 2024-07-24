import pandas as pd

def get_pokemon_df(pokemon_all):
    pokemon_list = []
    for i in pokemon_all:
        pokemon_list.append(i)
    pokemon_df = pd.DataFrame(pokemon_list)
    return pokemon_df

# Function to calculate a combined score (optional)
def calculate_combined_score(row):
    # Example: Sum of all criteria columns
    return row['HP Max'] + row['Defense Max'] + row['Speed Max'] + row['Special Attack Max'] + row['Special Defense Max'] + row['Attack Max']

def top_pokemon(pokemon_all):
    df = get_pokemon_df(pokemon_all)
    criteria_columns = ['HP Max', 'Defense Max', 'Speed Max', 'Special Attack Max', 'Attack Max', 'Special Defense Max', 'Defense Max']

    # Calculate thresholds for top 1% for each criteria column
    thresholds = {}
    for col in criteria_columns:
        thresholds[col] = df[col].quantile(0.98)

    # Apply combined score calculation
    df['Combined Score'] = df.apply(calculate_combined_score, axis=1)

    # Sort DataFrame by combined score or individual criteria columns
    sorted_df = df.sort_values(by='Combined Score', ascending=False)

    # Select top 2% based on combined score or individual criteria columns
    top_2_percent_threshold = sorted_df['Combined Score'].quantile(0.98)
    top_2_percent_pokemon = sorted_df[sorted_df['Combined Score'] >= top_2_percent_threshold]

    # Display the top 2% Pokémon
    json_data = top_2_percent_pokemon.to_json(orient='records')
    return json_data