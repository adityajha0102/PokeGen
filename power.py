import random

type_chart = {
    'Normal': {'Rock': 0.75, 'Ghost': 0.3, 'Steel': 0.75},
    'Fire': {'Fire': 0.75, 'Water': 0.75, 'Grass': 1.25, 'Ice': 1.25, 'Bug': 1.25, 'Rock': 0.75, 'Dragon': 0.75, 'Steel': 1.25},
    'Water': {'Fire': 1.25, 'Water': 0.75, 'Grass': 0.75, 'Ground': 1.25, 'Rock': 1.25, 'Dragon': 0.75},
    'Electric': {'Water': 1.25, 'Electric': 0.75, 'Grass': 0.75, 'Ground': 0.3, 'Flying': 1.25, 'Dragon': 0.75},
    'Grass': {'Fire': 0.75, 'Water': 1.25, 'Grass': 0.75, 'Poison': 0.75, 'Ground': 1.25, 'Flying': 0.75, 'Bug': 0.75, 'Rock': 1.25, 'Dragon': 0.75, 'Steel': 0.75},
    'Ice': {'Fire': 0.75, 'Water': 0.75, 'Grass': 1.25, 'Ice': 0.75, 'Ground': 1.25, 'Flying': 1.25, 'Dragon': 1.25, 'Steel': 0.75},
    'Fighting': {'Normal': 1.25, 'Ice': 1.25, 'Poison': 0.75, 'Flying': 0.75, 'Psychic': 0.75, 'Bug': 0.75, 'Rock': 1.25, 'Ghost': 0.3, 'Dark': 1.25, 'Steel': 1.25, 'Fairy': 0.75},
    'Poison': {'Grass': 1.25, 'Poison': 0.75, 'Ground': 0.75, 'Rock': 0.75, 'Ghost': 0.75, 'Steel': 0.3, 'Fairy': 1.25},
    'Ground': {'Fire': 1.25, 'Electric': 1.25, 'Grass': 0.75, 'Poison': 1.25, 'Flying': 0.3, 'Bug': 0.75, 'Rock': 1.25, 'Steel': 1.25},
    'Flying': {'Electric': 0.75, 'Grass': 1.25, 'Fighting': 1.25, 'Bug': 1.25, 'Rock': 0.75, 'Steel': 0.75},
    'Psychic': {'Fighting': 1.25, 'Poison': 1.25, 'Psychic': 0.75, 'Dark': 0.3, 'Steel': 0.75},
    'Bug': {'Fire': 0.75, 'Grass': 1.25, 'Fighting': 0.75, 'Poison': 0.75, 'Flying': 0.75, 'Psychic': 1.25, 'Ghost': 0.75, 'Dark': 1.25, 'Steel': 0.75, 'Fairy': 0.75},
    'Rock': {'Fire': 1.25, 'Ice': 1.25, 'Fighting': 0.75, 'Ground': 0.75, 'Flying': 1.25, 'Bug': 1.25, 'Steel': 0.75},
    'Ghost': {'Normal': 0.3, 'Psychic': 1.25, 'Ghost': 1.25, 'Dark': 0.75},
    'Dragon': {'Dragon': 1.25, 'Steel': 0.75, 'Fairy': 0.3},
    'Dark': {'Fighting': 0.75, 'Psychic': 1.25, 'Ghost': 1.25, 'Dark': 0.75, 'Fairy': 0.75},
    'Steel': {'Fire': 0.75, 'Water': 0.75, 'Electric': 0.75, 'Ice': 1.25, 'Rock': 1.25, 'Steel': 0.75, 'Fairy': 1.25},
    'Fairy': {'Fire': 0.75, 'Fighting': 1.25, 'Poison': 0.75, 'Dragon': 1.25, 'Dark': 1.25, 'Steel': 0.75}
}


def type_effectiveness(attacker_type, defender_type):
    if attacker_type in type_chart and defender_type in type_chart[attacker_type]:
        return type_chart[attacker_type][defender_type]
    return 1  # Neutral effectiveness if not specified


def calculate_power_score(pokemon, opponent_type):
    # Use average of min and max for each stat
    hp = (pokemon['HP Min'] + pokemon['HP Max']) / 2
    attack = (pokemon['Attack Min'] + pokemon['Attack Max']) / 2
    defense = (pokemon['Defense Min'] + pokemon['Defense Max']) / 2
    speed = (pokemon['Speed Min'] + pokemon['Speed Max']) / 2
    special_attack = (pokemon['Special Attack Min'] + pokemon['Special Attack Max']) / 2
    special_defense = (pokemon['Special Defense Min'] + pokemon['Special Defense Max']) / 2

    # Calculate type effectiveness
    effectiveness = type_effectiveness(pokemon["Simplified Type"], opponent_type)

    # Calculate power score with type effectiveness
    power_score = (hp * 0.15 +
                   attack * 0.2 * effectiveness +
                   defense * 0.15 +
                   speed * 0.1 +
                   special_attack * 0.2 * effectiveness +
                   special_defense * 0.15)

    return power_score


def compare_pokemon(pokemon1, pokemon2):
    score1 = calculate_power_score(pokemon1, pokemon2["Simplified Type"])
    score2 = calculate_power_score(pokemon2, pokemon1["Simplified Type"])

    if score1 > score2:
        return pokemon1, pokemon2
    elif score2 > score1:
        return pokemon2, pokemon1
    else:
        if random.choice([pokemon1, pokemon2])==pokemon1:
            return pokemon2, pokemon1
        else:
            return pokemon1, pokemon2
