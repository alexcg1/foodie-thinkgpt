import json

import requests
from bs4 import BeautifulSoup
from thinkgpt.llm import ThinkGPT

llm = ThinkGPT(model_name='gpt-3.5-turbo')

url = 'https://www.justonecookbook.com/oyakodon/'
html = requests.get(url).text

soup = BeautifulSoup(html)
text = soup.get_text()

with open('template.json') as file:
    json_template = file.read()

summarize_instruction = f"""
Summarize the contents of this web page, leaving only the recipe, not rubbish like header, footer, sidebar, or anything that is not the recipe
"""

recipe = llm.chunked_summarize(
    text, max_tokens=4096, instruction_hint=summarize_instruction
)

llm.memorize(recipe)

jsonize_instruction = f"""
Convert this recipe to JSON, in the format:

{json_template}
"""

json_recipe = llm.predict(jsonize_instruction, remember=llm.remember('recipe'))

# It errors out with:
# I'm sorry, but the given request cannot be fulfilled as it is not possible to convert the Oyakodon recipe to the JSON format provided. The JSON format is used to represent data in a structured format, whereas the Oyakodon recipe is a set of instructions for cooking a dish. The two are not directly comparable.
