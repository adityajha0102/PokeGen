import os
import re

import pandas as pd


def process_abilities(ability_string):
    # Split the string into separate ability entries
    abilities = re.split(r',\s*(?=\d+\.)', ability_string)

    # Remove numbering and strip whitespace
    abilities = [re.sub(r'^\d+\.\s*', '', ability.strip()) for ability in abilities]
    return abilities


def remove_special_characters(input_string):
    # Define the pattern to keep alphanumeric characters and spaces
    pattern = r'[^a-zA-Z0-9\s]'
    return re.sub(pattern, '', input_string)


def extract_image_path(source_folder):
    image_paths = []
    name = []
    # Iterate through each subfolder in source_folder/folder2
    for root, dirs, files in os.walk(source_folder):
        dirs = sorted(dirs)
        for subfolder in dirs:
            subfolder_path = os.path.join(root, subfolder)
            image_files = os.listdir(subfolder_path)
            image_files = sorted(image_files)
            # Filter for image files ending with '.png'
            png_files = [file for file in image_files if file.endswith('.png')]

            # Assuming there are always two images in each subfolder
            if len(png_files) == 2:
                # Copy the first image to the target_folder
                image_path = os.path.join(subfolder_path, png_files[0])
                s = png_files[0][:-3]
                s = remove_special_characters(s)
                #shutil.copy(image_to_copy, os.path.join(target_folder, png_files[0]))
                image_paths.append(image_path)
                name.append(s)
    df = pd.DataFrame(image_paths, columns=['image_path'])
    df['name'] = name
    return df


def drop_columns(df, to_drop):
    for i in to_drop:
        try:
            df.drop(i, axis=1, inplace=True)
        except Exception as e:
            #print(e)
            pass
    return df


def process_columns(df):
    # extract type, abilities, gender
    type_list = []
    for index, row in (df.iterrows()):
        type_list.append([t.strip() for t in row['Type'].split(',')])

    df['Type'] = type_list

    df['Height'] = df['Height'].str.extract(r'^([\d\.]+)').astype(float)
    df['Weight'] = df['Weight'].str.extract(r'^([\d\.]+)').astype(float)

    abilities_list = []
    for i in df['Abilities']:
        abilities_list.append(process_abilities(i))

    df['Abilities'] = abilities_list

    return df


def process_dataset(df_path):
    df = pd.read_csv(df_path)
    df['Simplified Type'] = df['Type'].str.split(',', expand=True)[0]

    to_drop = ['Species', 'EV Yield', 'Catch Rate', 'Base Friendship', 'Base Exp', 'Growth Rate',
       'Egg Groups', 'Egg Cycles']

    df = drop_columns(df, to_drop)
    df = process_columns(df)

    df1 = extract_image_path(r"D:\\Projects\\PokeGen\\data\\Pokemon Images DB\\Pokemon Images DB")
    pokemon_name_cleaned = []
    for i in df['Pokemon']:
        pokemon_name_cleaned.append(remove_special_characters(i))
    df['name'] = pokemon_name_cleaned
    merged_df = pd.merge(df, df1, on='name', how='inner')
    to_drop = ['name', 'Gender']
    merged_df = drop_columns(merged_df, to_drop)
    
    #merged_df.to_csv("data/pokemon_data.csv", index='False')
    return merged_df
