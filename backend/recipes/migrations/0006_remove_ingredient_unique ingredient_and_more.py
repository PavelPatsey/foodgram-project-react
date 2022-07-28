# Generated by Django 4.0.6 on 2022-07-28 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0005_alter_ingredient_unique_together_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="ingredient",
            name="unique ingredient",
        ),
        migrations.AlterUniqueTogether(
            name="ingredient",
            unique_together={("name", "measurement_unit")},
        ),
    ]