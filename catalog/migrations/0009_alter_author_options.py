# Generated by Django 5.0.6 on 2024-07-09 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name']},
        ),
    ]
