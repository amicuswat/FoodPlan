from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    telegram_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    is_manager = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    USERNAME_FIELD = 'telegram_id'

class Dish(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    picture = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title


class DishStep(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    order = models.IntegerField()
    picture = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Product(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class DishProduct(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.CharField(max_length=200)


class UserDish(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)
    shown_date_time = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class UsedTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)


