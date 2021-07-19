import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django Command to pause execution until DB is up & ready
    """

    def handle(self, *args, **options):
        self.stdout.write("Waiting For Database ...")
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write(self.style.WARNING('Database is not available !'))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database is available '))
