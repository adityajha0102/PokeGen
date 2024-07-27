from helpers.prompts import get_details
from helpers.response_parser import extract_pokemon_details 

def hp_stats(base_hp):
  #Calculate max and min hp from base hp

  initial_base_hp = 10
  initial_min_hp = 130
  initial_max_hp = 224

  score = (base_hp-initial_base_hp)*2
  min_hp = initial_min_hp+score
  max_hp = initial_max_hp+score
  
  return min_hp, max_hp


def minmax_stats(base_stat):
  #Calculate max and min stat from base stat

  initial_base_stat = 10
  initial_min_stat = 22
  initial_max_stat = 130

  score = (base_stat-initial_base_stat)
  min_stat = initial_min_stat+((score//5)*9)
  max_stat = initial_max_stat+((score//5)*11)
  
  if score%5>=3:
    min_stat+=((score%5)*2)-1
  else:
    min_stat+=(score%5)*2
  if score%5>=1:
    max_stat+=((score%5)*2)+1
  return(min_stat, max_stat)


def get_info(client, description):
  prompt = get_details(description)
  response = client.invoke(prompt)
  name, type, height, weight, abilities, backstory = extract_pokemon_details(response)
  return name, type, height, weight, abilities, backstory
