# Generated by Django 5.1.7 on 2025-05-09 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("join_app", "0004_profile"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="color_hex",
            new_name="color",
        ),
    ]
