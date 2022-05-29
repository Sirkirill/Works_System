from rest_framework import serializers

from work.models import Work, People


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['full_name']


class WorkSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True)

    class Meta:
        model = Work
        fields = ['title', 'iswc', 'contributors']
        lookup_field = ['iswc']