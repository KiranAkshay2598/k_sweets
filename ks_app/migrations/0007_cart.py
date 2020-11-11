# Generated by Django 3.1 on 2020-10-24 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ks_app', '0006_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=300)),
                ('phone_number', models.BigIntegerField(max_length=10)),
                ('email', models.CharField(max_length=300)),
                ('address', models.CharField(max_length=1000)),
                ('cart_item', models.ManyToManyField(to='ks_app.CartItem')),
            ],
        ),
    ]
