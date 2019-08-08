from rest_framework import serializers


class FacultySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    university_id = serializers.IntegerField()
    orcid = serializers.IntegerField(required=False, read_only=True)
    scopus = serializers.IntegerField(required=False, read_only=True)
    google_scholar = serializers.IntegerField(required=False, read_only=True)
    semantic_scholar = serializers.IntegerField(required=False, read_only=True)
    wos = serializers.IntegerField(required=False, read_only=True)
