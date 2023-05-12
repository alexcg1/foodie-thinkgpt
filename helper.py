import json
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseModel
from rich import print
from serpapi import GoogleSearch
from thinkgpt.llm import ThinkGPT

load_dotenv()

llm = ThinkGPT(model_name='gpt-3.5-turbo', temperature=0)


class Recipe(BaseModel):
    name: str = ''
    text: str = ''
    full_text: str = ''
    ingredients: list = []
    directions: list = []
    url: AnyHttpUrl | None


def get_suggestions(nationality: str):
    """
    Get dish suggestions
    """
    pass


def translate_term(term: str, language: str, append: str = 'recipe'):
    pass


def search_recipes(query: str):
    search = GoogleSearch({'q': query, 'api_key': os.environ['SERP_API_KEY']})
    results = search.get_dict()['organic_results']

    output = []
    for result in results:
        print(result)
        output.append(
            {
                'url': result['link'],
                'title': result['title'],
                'snippet': result['snippet'],
            }
        )

    return output


def get_web_text(url):
    response = requests.get(url)

    # fix encoding
    response.encoding = response.apparent_encoding

    html = response.text

    # Extract all text
    soup = BeautifulSoup(html)
    text = soup.get_text()

    return text


def extract_recipe_text(text, recipe_name):
    # Remove crap
    summarize_instruction = f"""
    Summarize the contents of this web page, leaving only the recipe for {recipe_name}.
    - If the recipe is not in English, translate it into English
    - Exclude junk like the header, footer, sidebar, and anything that is NOT the recipe
    """

    recipe_text = llm.chunked_summarize(
        text, max_tokens=4096, instruction_hint=summarize_instruction
    )

    return recipe_text


def extract_ingredients(text):
    ingredients = llm.predict(
        """
        what are the ingredients of this recipe?
        - return the output as a simple JSON list
        - use the keys "quantity" and "ingredient"
        - Do not assign a key to the list itself.
        - Do not add number keys to the list
        - Ensure you list ALL ingredients. Do not skip any
        - Use this format:

        <!--json-format-start-->
        [
          {"quantity": "2 tbsp", "ingredient": "ingredient_name"},
          {"quantity": "20 grams", "ingredient": "ingredient_name"},
          {"quantity": "unspecified", "ingredient": "ingredient_name"},
        ]
        <!--json-format-end-->
        """,
        remember=[text],
    )

    recipe_ingredients = json.loads(ingredients)

    return recipe_ingredients


def extract_directions(text):
    directions = llm.predict(
        'what are the directions of this recipe? return the output as a simple JSON list. Do not give the list a key. do not number the list items. Ensure it is valid JSON',
        remember=[text],
    )

    directions = json.loads(directions)

    return directions
