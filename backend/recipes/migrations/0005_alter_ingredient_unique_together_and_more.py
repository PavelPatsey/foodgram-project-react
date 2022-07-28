# Generated by Django 4.0.6 on 2022-07-28 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0004_alter_tag_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="ingredient",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="tag",
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name="ingredient",
            constraint=models.UniqueConstraint(
                fields=("name", "measurement_unit"), name="unique ingredient"
            ),
        ),
    ]
