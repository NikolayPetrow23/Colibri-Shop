# Generated by Django 4.2.2 on 2023-09-03 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbrands',
            name='image',
            field=models.ImageField(blank=True, upload_to='brands_images'),
        ),
    ]
