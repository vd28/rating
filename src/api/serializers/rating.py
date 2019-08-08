from rest_framework import serializers
from . import BaseRatingSerializer


class FacultyRatingSerializer(BaseRatingSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    university_id = serializers.IntegerField()


class DepartmentRatingSerializer(BaseRatingSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    faculty_id = serializers.IntegerField()


class PersonRatingSerializer(BaseRatingSerializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    department_id = serializers.IntegerField()
    person_type_ids = serializers.SerializerMethodField()

    def get_person_type_ids(self, instance):
        return [person_type.id for person_type in instance.person_types.all()]


class BaseRatingOptionsSerializer(serializers.Serializer):
    SCOPUS = 'scopus'
    GOOGLE_SCHOLAR = 'google-scholar'
    SEMANTIC_SCHOLAR = 'semantic-scholar'
    WOS = 'wos'
    SNAPSHOTS = (SCOPUS, GOOGLE_SCHOLAR, SEMANTIC_SCHOLAR, WOS)

    revision_id = serializers.IntegerField(required=False)
    snapshot = serializers.ChoiceField(choices=SNAPSHOTS)


class PersonRatingOptionsSerializer(BaseRatingOptionsSerializer):
    university_id = serializers.IntegerField(required=False)
    faculty_id = serializers.IntegerField(required=False)
    department_id = serializers.IntegerField(required=False)
    person_type_ids = serializers.ListField(child=serializers.IntegerField(), required=False)

    def validate(self, attrs):
        if [attrs.get('university_id'), attrs.get('faculty_id'), attrs.get('department_id')].count(None) != 2:
            raise serializers.ValidationError(
                "One of these fields are required: 'university_id', 'faculty_id' or 'department_id'."
            )
        return attrs


class FacultyRatingOptionsSerializer(BaseRatingOptionsSerializer):
    university_id = serializers.IntegerField()


class DepartmentRatingOptionsSerializer(BaseRatingOptionsSerializer):
    university_id = serializers.IntegerField(required=False)
    faculty_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        if [attrs.get('university_id'), attrs.get('faculty_id')].count(None) != 1:
            raise serializers.ValidationError("One of these fields are required: 'university_id', 'faculty_id'.")
        return attrs
