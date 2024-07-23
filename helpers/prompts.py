def verify_prompt(user_prompt):
  return f"""Your task is to verify the user-provided prompt.
Return yes if it mentions about any Pokémon; otherwise, return no.

The answer should be in below format:
answer:
[answer]

Here is the user prompt you need to verify:

    {user_prompt}

Do not generate anything else.
"""

def modify_prompt(user_prompt):
  return f"""Your task is to modify the prompt provided by user.
Return the modified prompt if it mentions about pokemon else return NULL.

Response format
1. Add a sentence mentioning that the background should be white.
2. Add a sentence asking to generate just a single picture of the Pokemon.
3. Add a sentence asking that the picture should be clear and accurate.
4. Keep the modified_prompt in 1-2 sentence only.
5. Strictly return in the below format only:
modified_prompt:
[modified_prompt]

Here is the user prompt you need to modify:

    ```
    {user_prompt}
    ```

Please generate the modified prompt based on the provided information only, following the specified structure and instructions carefully.
"""

def get_details(description):
  return f"""Your task is to generate stats of a Pokemon based on the given description.
Return the Name, Type, Height, Weight, Abilities and Back Story of the Pokemon.

Response format
1. Type - Get the type of the Pokemon from its {description}.
2. Pokemon - Generate a new Pokemon name based on its Type that does not exist.
3. Height - Height of the Pokemon from its {description}.
4. Weight - Weight of the Pokemon from its {description}.
5. Abilities - Abilities based on its Type and its usefulness in battles.
e.g.
- Synchronize
- Inner Focus, Magic Guard (hidden ability)
6. BackStory - Create a new and unique back story for the Pokemon in 2-3 sentences.
7. Strictly return in the below format only:
Pokemon:
[Pokemon]
Type:
[Type]
Height:
[Height in meters between 1-90] meters
Weight:
[Weight in kg between 5-950] kg
Abilities:
[Abilities]
BackStory:
[BackStory]

Here are the description and type of the Pokemon you need to use to generate the stats:

    ```
    {description}
    ```

Please generate the information based on the provided format only, following the specified structure and instructions carefully.
Do not generate anything else instead.
"""

def get_story(pokemon1, pokemon2):
  return f"""Your task is to compare the given stats of two Pokemons and determine why {pokemon1} would win in a battle against {pokemon2}.
Return why the {pokemon1} won and how the battle went on.

Response format
1. winning_explaination - 3 bullet points explanation of why the given Pokemon won.
2. Each bullet point should only explain the aspects that proved advantageous.
winning aspects like Type Advantage, Power, Agility and Speed and Strategic Use of Environment.
e.g.
- Pikachu's Electric-type moves are super effective against Onix, which is a Rock/Ground type. Electric-type moves deal double damage to Onix due to its Rock typing.
- Pikachu is known for its speed and agility. It can dodge Onix's attacks and deliver quick, precise strikes, potentially outmaneuvering the slower Onix.
- Pikachu might use its surroundings cleverly in a battle against Onix. It could exploit terrain features or use electrically conductive surfaces to its advantage, enhancing the power of its Electric-type moves.
3. Do not list down the numerical stats of the Pokemon.
4. Keep the winning_explaination in 1-2 sentence only.
5. battle_story - In 5-6 sentences how the battle went on between the two Pokemons and how {pokemon1} won the battle.
6. Properly describe the environment in which the battle is taking place and all the different types of attack each Pokemon did.
7. Strictly return in the below format only:
winning_explaination:
[winning_explaination]
battle_story:
[battle_story]

Here are the Pokemons you need to be compare:

    ```
    {pokemon1}
    {pokemon2}
    ```

Please generate the winning explaination and battle story based on the provided information only, following the specified structure and instructions carefully.
"""