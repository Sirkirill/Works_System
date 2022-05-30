import csv
import re

from django.core.management import BaseCommand

from work.models import Work


class Command(BaseCommand):
    help = 'Collect work from csv file'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        file = options['file'][0]
        with open(file, 'rt') as file:
            works = csv.reader(file)
            row = 0
            for work in works:
                if row == 0:
                    row += 1
                else:
                    iswc = work[2]
                    contributors = re.sub(" +", " ", work[1]).strip().split('|')
                    title = work[0]
                    current_work = Work.objects.filter(iswc=iswc)
                    if iswc and current_work.exists():  # if work with  current iswc exist
                        current_work.first().update_current_work(title, iswc, contributors)
                    else:
                        probable_works = Work.objects.filter(title=title, contributors__full_name__in=contributors)
                        if probable_works.exists():  # if work with same title and at least one same contributor exist
                            for current_work in probable_works.all():
                                current_work.update_current_work(title, iswc, contributors)
                        else:  # if wee need to create new work
                            current_work = Work.objects.create()
                            current_work.update_current_work(title, iswc, contributors)
