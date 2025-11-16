"""Auto-generated migration for Rating model.

This migration was added manually to ensure tests run in the test database.
"""
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("bookMng", "0002_book"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="bookMng.book"),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
                ("value", models.PositiveIntegerField(default=1)),
            ],
            options={
                "unique_together": {("book", "user")},
            },
        ),
    ]
