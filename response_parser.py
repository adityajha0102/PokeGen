import re

def extract_pokemon_verification(response):
    # Initialize sections dictionary
    sections = {}

    # Extract modified_prompt
    answer = re.search(r'answer:(.*?)(?:\n\n|\Z)', response, re.DOTALL)
    if answer:
        sections['answer'] = answer.group(1).strip()

    return sections


def extract_modified_pokemon_prompt(response):
    # Initialize sections dictionary
    sections = {}

    # Extract modified_prompt
    modified_prompt = re.search(r'modified_prompt:(.*?)(?:\n\n|\Z)', response, re.DOTALL)
    if modified_prompt:
        sections['modified_prompt'] = modified_prompt.group(1).strip()

    return sections


def extract_pokemon_details(response):
    # Initialize sections dictionary
    sections = {}
    
    # Extract Pokemon name
    pokemon = re.search(r'Pokemon:\s*(\w+)', response, re.DOTALL)
    if pokemon:
        sections['Pokemon'] = pokemon.group(1).strip()

    # Extract Pokemon type
    type = re.search(r'Type:\s*(\w+)', response, re.DOTALL)
    if type:
        sections['Type'] = type.group(1).strip()

    # Extract Pokemon height
    type = re.search(r'Height:\s*([\d\.]+)', response, re.DOTALL)
    if type:
        sections['Height'] = float(type.group(1).strip())

    # Extract Pokemon weight
    type = re.search(r'Weight:\s*([\d\.]+)', response, re.DOTALL)
    if type:
        sections['Weight'] = float(type.group(1).strip())

    # Extract Abilities
    abilities = re.search(r'Abilities:(.*?)(?=^\w+:|\Z)', response, re.DOTALL | re.MULTILINE)
    if abilities:
        sections['Abilities'] = abilities.group(1).strip()
    
    abilities_list = process_abilities(sections['Abilities'])

    # Extract Back Story
    back_story = re.search(r'BackStory:(.*?)(?=^\w+:|\Z)', response, re.DOTALL | re.MULTILINE)
    if back_story:
        sections['BackStory'] = back_story.group(1).strip()

    return sections['Pokemon'], sections['Type'], sections['Height'], sections['Weight'], abilities_list, sections['BackStory']

def process_abilities(ability_string):
    # Split the string into separate ability entries
    abilities = re.split(r'\n*-\s*', ability_string)

    # Remove empty strings from the list
    abilities = [ability.strip() for ability in abilities if ability.strip()]

    return abilities

def extract_story(response):
    # Initialize sections dictionary
    sections = {}

    # Extract winning_explanation
    winning_match = re.search(r'winning_explaination:(.*?)(?:\n\n|\Z)', response, re.DOTALL)
    if winning_match:
        sections['winning_explanation'] = winning_match.group(1).strip()

    # Extract battle_story
    battle_match = re.search(r'battle_story:(.*?)(?=^\w+:|\Z)', response, re.DOTALL | re.MULTILINE)
    if battle_match:
        sections['battle_story'] = battle_match.group(1).strip()

    return sections