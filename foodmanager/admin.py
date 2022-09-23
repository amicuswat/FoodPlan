from django.contrib import admin
from .models import User, Dish, DishStep, Product, DishProduct, UserDish, Tag, UsedTag

admin.site.register(User)
admin.site.register(Dish)
admin.site.register(DishStep)
admin.site.register(Product)
admin.site.register(DishProduct)
admin.site.register(UserDish)
admin.site.register(Tag)
admin.site.register(UsedTag)
