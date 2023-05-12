from fastapi import FastAPI
from rich import print

from helper import (Recipe, extract_directions, extract_ingredients,
                    extract_recipe_text, get_web_text, search_recipes)

recipe = Recipe()
app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'hello world'}


@app.get('/search')
async def search(query: str):
    return search_recipes(query)


@app.get('/recipe')
async def get_recipe():
    recipe.url = 'https://www.sirogohan.com/sp/recipe/tenpura/'
    recipe.name = 'Tempura'  # in future get this from the web content
    recipe_full_text = get_web_text(recipe.url)

    # with open('template.json') as file:
    # json_template = file.read()

    # with open('ingredients.json') as file:
    # ingredients_template = file.read()

    recipe.text = extract_recipe_text(recipe_full_text, recipe.name)
    recipe.ingredients = extract_ingredients(recipe.text)
    recipe.directions = extract_directions(recipe.text)

    print(recipe)

    recipe_json = recipe.json()

    return recipe_json
