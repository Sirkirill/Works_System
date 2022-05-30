import argparse
import csv
import re

from django.core.management import BaseCommand

from work.models import Work
from work.views import has_duplicate_contributors


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
                        probable_works = Work.objects.filter(title=title)
                        probable_works_contributors = probable_works.values("contributors__full_name").all()
                        if probable_works.exists() and has_duplicate_contributors(
                                contributors,
                                probable_works_contributors
                        ):  # if work with same title and at least one same contributor exist
                            for current_work in probable_works.all():
                                current_work_contributors = current_work.contributors.values("full_name").all()
                                if has_duplicate_contributors(contributors, current_work_contributors):
                                    # check if current work has at least one same contributor
                                    current_work.update_current_work(title, iswc, contributors)
                        else:  # if wee need to create new work
                            current_work = Work.objects.create()
                            current_work.update_current_work(title, iswc, contributors)
