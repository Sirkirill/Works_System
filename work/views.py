import csv
import re

from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View
from rest_framework import viewsets
from rest_framework.response import Response

from work.models import Work
from work.serializer import WorkSerializer


def has_duplicate_contributors(contributors, probable_work):
    return any(list(contributor.values())[0] in contributors for contributor in list(probable_work))


class HomeView(View):
    def get(self, request):
        return render(request, "work.html", context={"queryset": Work.objects.all()})


class WorksView(View):
    def post(self, request):
        file = request.FILES['myfile']
        with open(file.name, 'rt') as file:
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
        return redirect(reverse('home'))


class WorksViewSet(viewsets.ViewSet):
    queryset = Work.objects.all()
    lookup_field = 'iswc'

    def retrieve(self, request, iswc=None):
        work = get_object_or_404(self.queryset, iswc=iswc)
        serializer = WorkSerializer(work)
        return Response(serializer.data)
