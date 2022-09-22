from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    telegram_id = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    is_manager = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)


class Dish(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()


class DishStep(models.Model):
    dish_primary_key = models.ForeignKey(Dish, on_delete=models.CASCADE)
    order = models.IntegerField()
    picture = models.CharField(max_length=100)
    description = models.TextField()


class Product(models.Model):
    title = models.CharField(max_length=200)


class DishProduct(models.Model):
    dish_primary_key = models.ForeignKey(Dish, on_delete=models.CASCADE)
    product_primary_key = models.ManyToManyField(Product)
    amount = models.CharField(max_length=200)


class UserDish(models.Model):
    dish_primary_key = models.ManyToManyField(Dish)
    user_primary_key = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)
    shown_date_time = models.DateTimeField()


class Tag(models.Model):
    title = models.CharField(max_length=200)


class UsedTag(models.Model):
    tag_primary_key = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
    dish_primary_key = models.ManyToManyField(Dish)
    product_primary_key = models.ManyToManyField(Product)
    user_primary_key = models.ManyToManyField(User)


