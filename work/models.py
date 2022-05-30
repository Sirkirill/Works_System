from django.db import models


class People(models.Model):
    full_name = models.CharField(verbose_name="Full name", max_length=255)


class Work(models.Model):
    title = models.CharField(verbose_name="Title", max_length=255)
    iswc = models.CharField(verbose_name="Iswc", max_length=255, blank=True, db_index=True)
    contributors = models.ManyToManyField(People, related_name="works", verbose_name="Contributors")

    def update_current_work(self, title, iswc, contributors):
        self.title = title
        if iswc:
            self.iswc = iswc
        for contributor in contributors:
            people = People.objects.get_or_create(full_name=contributor)[0]
            self.contributors.add(people)
        self.save()
