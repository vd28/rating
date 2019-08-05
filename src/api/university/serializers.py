from rest_framework import serializers
from core.models import Faculty


class FacultySerializer(serializers.ModelSerializer):
    orcid = serializers.IntegerField(default=0)
    scopus = serializers.IntegerField(default=0)
    google_scholar = serializers.IntegerField(default=0)
    semantic_scholar = serializers.IntegerField(default=0)
    wos = serializers.IntegerField(default=0)

    class Meta:
        model = Faculty
        fields = ('id', 'name', 'university_id', 'orcid', 'scopus', 'google_scholar', 'semantic_scholar', 'wos')
