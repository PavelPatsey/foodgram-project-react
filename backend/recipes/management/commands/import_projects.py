import csv

from approve_projects.models import Project
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import Users from `static/data/projects_example.csv`"

    def handle(self, *args, **kwargs):
        with open("static/data/projects_example.csv", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                print(row)
                Project.objects.create(
                    last_name=row[1],
                    first_name=row[2],
                    patronymic=row[3],
                    title=row[5],
                    description=row[6],
                )
