# Generated by Django 4.0.2 on 2022-03-17 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0020_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(default='order_', max_length=150),
        ),
    ]
