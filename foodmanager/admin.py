from django.contrib import admin
from .models import User, Dish, DishStep, Product, DishProduct, UserDish, Tag, \
    UsedTag

class DishStepInline(admin.TabularInline):
    model = DishStep

class DishProductsInline(admin.TabularInline):
    model = DishProduct

class UsedTagInline(admin.TabularInline):
    model = UsedTag

class DishAdmin(admin.ModelAdmin):
    inlines = [
        UsedTagInline,
        DishStepInline,
        DishProductsInline,
    ]

admin.site.register(User)
admin.site.register(Dish, DishAdmin)
admin.site.register(DishStep)
admin.site.register(Product)
admin.site.register(DishProduct)
admin.site.register(UserDish)
admin.site.register(Tag)
admin.site.register(UsedTag)
