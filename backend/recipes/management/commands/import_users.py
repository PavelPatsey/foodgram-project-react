import csv

from approve_projects.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = "Import Users from `static/data/users_example.csv`"

    def handle(self, *args, **kwargs):
        with open("static/data/users_example.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",", quotechar="|")
            next(reader)
            for row in reader:
                User.objects.create(
                    username=get_random_string(20),
                    last_name=row[0],
                    first_name=row[1],
                    patronymic=row[2],
                    email=row[3],
                    telegram=row[4],
                    uid=get_random_string(100),
                )
