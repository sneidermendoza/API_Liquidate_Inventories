# Generated by Django 4.2 on 2024-08-26 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproducts',
            name='code',
            field=models.BigIntegerField(null=True, verbose_name='Codigo del Producto'),
        ),
        migrations.AlterField(
            model_name='historicalproducts',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Descripcion'),
        ),
        migrations.AlterField(
            model_name='products',
            name='code',
            field=models.BigIntegerField(null=True, verbose_name='Codigo del Producto'),
        ),
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Descripcion'),
        ),
    ]