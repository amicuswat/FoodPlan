import requests
import os
import time
from bs4 import BeautifulSoup
from foodmanager.models import Dish, DishStep, Product, DishProduct, Tag, UsedTag


def main():
	# process_nongluten_recipes()
	process_nonlactose_recipes()
	prodess_vegetarian_recipes()


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


def save_data(url, tag):
	for recipe_header in get_imcoock_recipe_header(url):
		is_dish_broken = False

		recipe_data = get_recipe_info(recipe_header)
		dishes = Dish.objects.filter(title=recipe_data['dish_title'])
		if not dishes:
			dish = Dish(title=recipe_data['dish_title'],
						description=recipe_data['dish_desc'],
						picture=recipe_data['dish_img_link'])
			dish.save()

			used_tag = UsedTag(tag=tag, dish=dish)
			used_tag.save()

			print(dish)
		else:
			print(f"такое блюдо есть {dishes[0]}")
			continue

		for step in recipe_data['steps']:
			step = DishStep(order=step['order'], dish=dish,
							picture=step['img_link'], description=step['desc'])
			step.save()

		for component in recipe_data['products']:

			try:

				ingredient = component[0]
				amount = component[1]
			except IndexError:
				is_dish_broken = True
				continue

			products = Product.objects.filter(title=ingredient)
			if not products:
				product = Product(title=ingredient)
				product.save()
			else:
				product = products[0]
			dish_product = DishProduct(product=product, dish=dish,
									   amount=amount)
			dish_product.save()
		if is_dish_broken:
			print(f" --- Удаляю сломанное блюдо {dish}")
			is_dish_broken = False
			dish.delete()


def get_tag(tag_name):
	tag = Tag.objects.filter(title=tag_name)
	if not tag:
		tag = Tag(title=tag_name)
		tag.save()
	else:
		tag = Tag.objects.filter(title=tag_name)[0]
	return tag


def process_nongluten_recipes():
	links = [f'https://www.iamcook.ru/event/baking/gluten-free-baking/{page+1}'
			 for page in range(4)]
	tag = get_tag("Без глютена")
	print("\n Загружаю блюда без глютена \n")

	for url in links:
		save_data(url, tag)


def process_nonlactose_recipes():
	url = "https://www.iamcook.ru/section/3551"

	tag = get_tag("Без Лактозы")
	print("\n Загружаю блюда без Лактозы \n")

	save_data(url, tag)

def prodess_vegetarian_recipes():
	links = [f"https://www.iamcook.ru/event/everyday/everyday-vegetarian/{page+1}"
			 for page in range(5)]

	tag = get_tag("Для вегитарианцев")
	print("\n Загружаю блюда для Веганов \n")

	for url in links:
		save_data(url, tag)


def image_download():
	pass


if __name__ == "__main__":
	main()
