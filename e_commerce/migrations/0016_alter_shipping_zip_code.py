# Generated by Django 4.0.2 on 2022-03-16 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0015_alter_shipping_address1_alter_shipping_address2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='zip_code',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
