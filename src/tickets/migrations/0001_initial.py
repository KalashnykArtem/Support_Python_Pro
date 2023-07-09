# Generated by Django 4.2.3 on 2023-07-05 17:34

from django.db import migrations, models

import tickets.constants


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
            ],
            options={
                "db_table": "messages",
            },
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("text", models.TextField()),
                ("visibility", models.BooleanField(default=True)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        default=tickets.constants.TicketStatus["NOT_STARTED"]
                    ),
                ),
            ],
            options={
                "db_table": "tickets",
            },
        ),
    ]