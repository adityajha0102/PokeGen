import os

import requests as r
from io import BytesIO
import base64

from helpers.prompts import verify_prompt, modify_prompt
from helpers.response_parser import extract_pokemon_verification, extract_modified_pokemon_prompt
from helpers.llm_utils import llm
from helpers.errors import ClientInvocationError


def get_Image(user_prompt):
    if user_prompt == "":
        raise ValueError("Provide a prompt.")
    preprocessed_prompt = process_generation_prompt(llm, user_prompt)
    img = generate_image(preprocessed_prompt['modified_prompt'])
    # Convert BytesIO to base64 string
    img_data = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_data

def process_generation_prompt(client, user_prompt):
    try:
        verification_prompt = verify_prompt(user_prompt)
        verification_response = client.invoke(verification_prompt)
        verification_response = extract_pokemon_verification(verification_response)
    except Exception as e:
        raise ClientInvocationError(f"An error occurred while invoking client: {e}")

    if verification_response['answer'] == "yes":
        try:
            modified_prompt = modify_prompt(user_prompt)
            modified_response = client.invoke(modified_prompt)
            modified_response = extract_modified_pokemon_prompt(modified_response)
        except Exception as e:
            raise ClientInvocationError(f"An error occurred while invoking client: {e}")

    elif verification_response['answer'] == "no":
        raise ValueError("This application can only generate Pokemon images. Try Again")
    else:
        raise ValueError("Something went wrong. Try a different text")

    return modified_response


def generate_image(prompt: str):
    payload = {"inputs": prompt,
               "parameters": {
                   "width": 768,
                   "height": 768,
                   "guidance_scale": 9
               }}
    headers = {
        "Authorization": f"Bearer {os.environ.get('HF_TOKEN')}",
        "Content-Type": "application/json",
        "Accept": "image/png"  # important to get an image back
    }
    response = r.post(os.environ.get('VISION_ENDPOINT'), headers=headers, json=payload)
    img = BytesIO(response.content)

    return img

