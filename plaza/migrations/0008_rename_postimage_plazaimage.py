# Generated by Django 5.0.2 on 2025-06-30 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plaza', '0007_alter_post_content'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostImage',
            new_name='PlazaImage',
        ),
    ]
