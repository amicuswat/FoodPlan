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

    def __str__(self):
        return self.title


class DishStep(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    order = models.IntegerField()
    picture = models.CharField(max_length=100)
    description = models.TextField()


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
    shown_date_time = models.DateTimeField()


class Tag(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class UsedTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


