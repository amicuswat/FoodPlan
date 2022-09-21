import requests
import time
from bs4 import BeautifulSoup



def parse_imcoock_page(url):
	response = requests.get(url)
	response.raise_for_status()
	soup = BeautifulSoup(response.text, 'html.parser')
	return soup.find_all("div", {"class": "header"})

def parse_imcoock_recipe(recipe_id):
	url = f"https://www.iamcook.ru{recipe_id}"
	response = requests.get(url)
	response.raise_for_status()
	soup = BeautifulSoup(response.text, 'html.parser')
	return soup

def parse_nongluten():
	for page in range(4):
		nongluten_url = f'https://www.iamcook.ru/event/baking/gluten-free-baking/{page}'
		for recipe in parse_imcoock_page(nongluten_url):
			recipe_id = recipe.find("a")["href"]
			recipe_response = parse_imcoock_recipe(recipe_id)
			recipe_name = recipe_response.find("h1", {"itemprop": "name"})
			recipe_description = recipe_response.find("span", {"itemprop": "description"}) # Может быть NullType, нужна проверка
			recipe_ingredients = recipe_response.find_all("p", {"itemprop": "recipeIngredient"})
			recipe_image = recipe_response.find("img", {"class": "resultphoto"})
			recipe_steps = recipe_response.find("div", {"class": "instructions"})
			steps = recipe_steps.find_all("p")
			for step in steps:
				if step.get_text() == "Подборка рецептов" or step.get_text() == "Коллекция рецептов": 	# Захардкожено, но подругому никак
					continue
			print(recipe_name.get_text())
			time.sleep(3)
def parse_nonlactose_cakes():
	nolactose_cakes_url = "https://www.iamcook.ru/section/3551"
	for recipe in parse_imcoock_page(nolactose_cakes_url):
		recipe_id = recipe.find("a")["href"]
		recipe_response = parse_imcoock_recipe(recipe_id)
		recipe_name = recipe_response.find("h1", {"itemprop": "name"})
		recipe_description = recipe_response.find("span", {"itemprop": "description"}) # Может быть NullType, нужна проверка
		recipe_ingredients = recipe_response.find_all("p", {"itemprop": "recipeIngredient"})
		recipe_image = recipe_response.find("img", {"class": "resultphoto"})
		recipe_steps = recipe_response.find("div", {"class": "instructions"})
		steps = recipe_steps.find_all("p")
		for step in steps:
			if step.get_text() == "Подборка рецептов" or step.get_text() == "Коллекция рецептов": 	# Захардкожено, но подругому никак
				continue
		print(recipe_name.get_text())
		time.sleep(3)


def image_download():
	pass


if __name__ == "__main__":
	parse_nongluten()
	parse_nonlactose_cakes()