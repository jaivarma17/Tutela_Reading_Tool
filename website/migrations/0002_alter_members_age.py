# Generated by Django 5.1 on 2024-08-13 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='age',
            field=models.IntegerField(),
        ),
    ]
