from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from Site.models import Circle

class Command(BaseCommand):
    help = 'Fetching Circle from Aapoon'

    def handle(self, **options):
        with connections['gcrmsserver'].cursor() as cursor:
            result = cursor.execute("SELECT * FROM social_groups_groups;")
            circles = cursor.fetchall()

            for circle in circles:
                link = circle[14]
                name = circle[3]
                group_id = circle[0]
                try:
                    circle = Circle.objects.get(group_id=group_id)
                    circle.link = link
                    circle.name = name
                    circle.save()
                    print("Update")
                except:
                    print("Create")
                    Circle.objects.create(link=link, name=name, group_id=group_id)
