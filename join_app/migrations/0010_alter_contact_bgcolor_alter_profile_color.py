# Generated by Django 5.1.7 on 2025-05-15 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("join_app", "0009_alter_contact_bgcolor_alter_profile_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="bgcolor",
            field=models.CharField(default="#b23d3e", max_length=10),
        ),
        migrations.AlterField(
            model_name="profile",
            name="color",
            field=models.CharField(default="#f5e971", max_length=10),
        ),
    ]
