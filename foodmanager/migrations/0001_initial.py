# Generated by Django 4.1.1 on 2022-09-22 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('telegram_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('is_manager', models.BooleanField(default=False)),
                ('is_premium', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserDish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.BooleanField(default=False)),
                ('disliked', models.BooleanField(default=False)),
                ('shown_date_time', models.DateTimeField()),
                ('dish_primary_key', models.ManyToManyField(to='foodmanager.dish')),
                ('user_primary_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodmanager.user')),
            ],
        ),
        migrations.CreateModel(
            name='UsedTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_primary_key', models.ManyToManyField(to='foodmanager.dish')),
                ('product_primary_key', models.ManyToManyField(to='foodmanager.product')),
                ('tag_primary_key', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='foodmanager.tag')),
                ('user_primary_key', models.ManyToManyField(to='foodmanager.user')),
            ],
        ),
        migrations.CreateModel(
            name='DishStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('picture', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('dish_primary_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodmanager.dish')),
            ],
        ),
        migrations.CreateModel(
            name='DishProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=200)),
                ('dish_primary_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodmanager.dish')),
                ('product_primary_key', models.ManyToManyField(to='foodmanager.product')),
            ],
        ),
    ]
