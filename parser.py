import requests
import time
from bs4 import BeautifulSoup



def get_imcoock_recipe_header(url):
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

def get_recipe_info(url):
	for recipe in get_imcoock_recipe_header(url):
			recipe_info = {}
			recipe_steps = []
			recipe_id = recipe.find("a")["href"]
			recipe_response = parse_imcoock_recipe(recipe_id)
			recipe_name = recipe_response.find("h1", {"itemprop": "name"})
			recipe_info["Название блюда"] = recipe_name.get_text()
			recipe_description = recipe_response.find("span", {"itemprop": "description"}) # Может быть NullType, нужна проверка
			if recipe_description:
				recipe_info["Описание блюда"] = recipe_description.get_text()
			recipe_ingredients = recipe_response.find_all("p", {"itemprop": "recipeIngredient"})
			for num, recipe_ingredient in enumerate(recipe_ingredients):
				recipe_info[f"{num}. Ингридиенты для блюда"] = recipe_ingredient.get_text()
			recipe_image = recipe_response.find("img", {"class": "resultphoto"})
			recipe_info["Ссылка на картинку блюда"] = recipe_image
			instructions = recipe_response.find("div", {"class": "instructions"})
			steps = instructions.find_all("p")
			for step in steps:
				if step.get_text() in ["Подборка рецептов", "Коллекция рецептов", "", "\n", " "]: # Захардкожено, но подругому никак
					continue
				step_img = step.find("img")
				recipe_steps.append(f"{len(recipe_steps)}. Шаг {step.get_text()} Картинка к шагу: {step_img}")
			recipe_info["Шаги приготовления: "] = recipe_steps
			time.sleep(3)
			print(recipe_info)


def parse_nongluten():
	for page in range(4):
		nongluten_url = f'https://www.iamcook.ru/event/baking/gluten-free-baking/{page+1}'
		return get_recipe_info(nongluten_url)


def parse_nonlactose_cakes():
	nolactose_cakes_url = "https://www.iamcook.ru/section/3551"
	return get_recipe_info(nolactose_cakes_url)

def parse_vegetarian_dishes():
	for page in range(5):
		vegetarian_dishes_url = f"https://www.iamcook.ru/event/everyday/everyday-vegetarian/{page+1}"
		return get_recipe_info(vegetarian_dishes_url)


def image_download():
	pass


if __name__ == "__main__":
	print(parse_nongluten())
	print(parse_nonlactose_cakes())
	print(parse_vegetarian_dishes())