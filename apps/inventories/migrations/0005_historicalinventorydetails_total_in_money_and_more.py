# Generated by Django 4.2 on 2024-08-22 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0004_historicalinventories_inventory_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalinventorydetails',
            name='total_in_money',
            field=models.PositiveIntegerField(null=True, verbose_name='total en dinero, calculodo multiplicando la cantidad del producto por el valor del producto'),
        ),
        migrations.AddField(
            model_name='inventorydetails',
            name='total_in_money',
            field=models.PositiveIntegerField(null=True, verbose_name='total en dinero, calculodo multiplicando la cantidad del producto por el valor del producto'),
        ),
    ]
