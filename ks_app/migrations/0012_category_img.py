# Generated by Django 3.1 on 2020-11-23 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ks_app', '0011_product_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='img',
            field=models.ImageField(default=None, null=True, upload_to='pics'),
        ),
    ]
