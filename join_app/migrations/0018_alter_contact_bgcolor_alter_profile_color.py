# Generated by Django 5.1.7 on 2025-05-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("join_app", "0017_alter_contact_bgcolor_alter_profile_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="bgcolor",
            field=models.CharField(default="#3a737c", max_length=10),
        ),
        migrations.AlterField(
            model_name="profile",
            name="color",
            field=models.CharField(default="#52796b", max_length=10),
        ),
    ]
