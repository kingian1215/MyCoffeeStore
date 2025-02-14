# Generated by Django 4.2.13 on 2024-07-13 17:21

import coffeebeans.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("coffeebeans", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="products",
            field=models.ManyToManyField(
                related_name="carts",
                through="coffeebeans.CartItem",
                to="coffeebeans.product",
            ),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="coffeebeans.cart",
            ),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart_items",
                to="coffeebeans.product",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="products",
            field=models.ManyToManyField(
                related_name="orders",
                through="coffeebeans.OrderItem",
                to="coffeebeans.product",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_items",
                to="coffeebeans.order",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                default="default.jpg", upload_to=coffeebeans.models.product_image_path
            ),
        ),
    ]
