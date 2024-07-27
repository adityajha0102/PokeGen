from helpers.power import compare_pokemon
from helpers.prompts import get_story
from helpers.llm_utils import llm
from helpers.response_parser import extract_story

def get_battle_details(pokemon1, pokemon2):
    winner, loser = compare_pokemon(pokemon1, pokemon2)
    battle_prompt = get_story(winner, loser)
    battle_response = llm.invoke(battle_prompt)
    result = extract_story(battle_response)
    return winner, result