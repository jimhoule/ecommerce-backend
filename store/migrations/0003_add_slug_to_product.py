# Generated by Django 3.2.4 on 2021-06-08 14:58

from django.db import migrations, models


class Migration(migrations.Migration):
	dependencies = [
		('store', '0002_rename_price_to_unit_price'),
	]

	operations = [
		migrations.AddField(
			model_name='product',
			name='slug',
			field=models.SlugField(default='-'),
			preserve_default=False,
		),
	]
