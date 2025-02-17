# Generated by Django 4.0.2 on 2022-03-14 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0006_alter_item_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favList_id', models.IntegerField(default=0, null=True)),
                ('name', models.CharField(default='favList', max_length=10)),
                ('item', models.ManyToManyField(to='e_commerce.Item')),
            ],
        ),
    ]
