from django.core.management.base import BaseCommand, CommandError
from dramasia.services import get_data_mdl

class Command(BaseCommand):

    def handle(self, *args, **options):
        data = [
            '15794-vanishing-time-a-boy-who-returned',
            '',
            '',
            '',
            '',
        ]
        for i in data:
            get_data_mdl(i)
