# Generated by Django 5.1 on 2024-08-13 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_articles'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Articles',
            new_name='Article',
        ),
        migrations.RenameModel(
            old_name='Members',
            new_name='Member',
        ),
    ]
