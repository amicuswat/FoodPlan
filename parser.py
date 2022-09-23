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

def get_recipe_info(recipe_header):
	recipe_id = recipe_header.find("a")["href"]
	recipe_response = parse_imcoock_recipe(recipe_id)

	recipe_name = recipe_response.find("h1", {"itemprop": "name"}) \
		.get_text()

	desc_html = recipe_response.find("span", {
		"itemprop": "description"})

	if not desc_html:
		recipe_description = None
	else:
		recipe_description = desc_html.get_text()

	products_html = recipe_response.find_all("p", {
		"itemprop": "recipeIngredient"})

	products = [elm.get_text().split(" - ") for elm in products_html]

	recipe_image = recipe_response.find("img",
										{"class": "resultphoto"})

	if recipe_image:
		recipe_image = recipe_image['src']

	steps_html = recipe_response \
		.find("div", {"class": "instructions"}) \
		.find_all("p")

	steps = []
	step_order = 1
	for step_html in steps_html:
		if step_html.get_text() not in ["Подборка рецептов",
										"Коллекция рецептов", "", "\n",
										" "]:
			img_link = step_html.find("img")
			if img_link:
				img_link = img_link['src']

			step = {
				"order": step_order,
				"img_link": img_link,
				"desc": step_html.get_text()
			}
			steps.append(step)
			step_order += 1

	recipe_data = {
		"dish_title": recipe_name,
		"dish_desc": recipe_description,
		"products": products,
		"dish_img_link": recipe_image,
		"steps": steps
	}

	time.sleep(3)
	return recipe_data


def process_nongluten_recipes():
	links = [f'https://www.iamcook.ru/event/baking/gluten-free-baking/{page+1}'
			 for page in range(4)]

	for url in links:
		for recipe_header in get_imcoock_recipe_header(url):
			recipe_data = get_recipe_info(recipe_header)
			print(recipe_data)



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
	process_nongluten_recipes()



	# print(parse_nonlactose_cakes())
	# print(parse_vegetarian_dishes())