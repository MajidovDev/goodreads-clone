# Generated by Django 4.1.7 on 2023-03-29 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_cover_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreview',
            name='created_at',
            field=models.DateTimeField(auto_created=True, null=True),
        ),
    ]
