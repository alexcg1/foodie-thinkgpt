import json

from pydantic import AnyHttpUrl, BaseModel
from rich import print
from thinkgpt.llm import ThinkGPT

from helper import get_web_text

llm = ThinkGPT(model_name='gpt-3.5-turbo', temperature=0)

# Define data model
class Recipe(BaseModel):
    name: str = ''
    ingredients: list = []
    directions: list = []
    url: AnyHttpUrl | None


recipe = Recipe()


# Get web page
recipe.name = 'Tempura'
recipe.url = 'https://www.sirogohan.com/sp/recipe/tenpura/'
text = get_web_text(recipe.url)

with open('template.json') as file:
    json_template = file.read()

with open('ingredients.json') as file:
    ingredients_template = file.read()

# Remove crap
summarize_instruction = f"""
Summarize the contents of this web page, leaving only the recipe for {recipe.name}.
- If the recipe is not in English, translate it into English
- Exclude junk like the header, footer, sidebar, and anything that is NOT the recipe
"""

recipe_text = llm.chunked_summarize(
    text, max_tokens=4096, instruction_hint=summarize_instruction
)

# extract ingredients
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
    remember=[recipe_text],
)

recipe.ingredients = json.loads(ingredients)

# extract directions
directions = llm.predict(
    'what are the directions of this recipe? return the output as a simple JSON list. Do not give the list a key. do not number the list items. Ensure it is valid JSON',
    remember=[recipe_text],
)

recipe.directions = json.loads(directions)
print(recipe)

recipe_json = recipe.json()
print(recipe_json)
