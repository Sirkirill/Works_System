import csv
import re

from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View
from rest_framework import viewsets
from rest_framework.response import Response

from work.models import Work
from work.serializer import WorkSerializer


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
                        probable_works = Work.objects.filter(title=title, contributors__full_name__in=contributors)
                        if probable_works.exists():  # if work with same title and at least one same contributor exist
                            for current_work in probable_works.all():
                                current_work.update_current_work(title, iswc, contributors)
                        else:  # if wee need to create new work
                            current_work = Work.objects.create()
                            current_work.update_current_work(title, iswc, contributors)
        return redirect(reverse('home'))


class WorksViewSet(viewsets.ViewSet):
    queryset = Work.objects.prefetch_related('contributors').all()
    lookup_field = 'iswc'

    def retrieve(self, request, iswc=None):
        work = get_object_or_404(self.queryset, iswc=iswc)
        serializer = WorkSerializer(work)
        return Response(serializer.data)
