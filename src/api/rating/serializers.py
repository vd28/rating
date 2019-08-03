from typing import Type
from rest_framework import serializers
from core import models


class BaseRatingSerializer(serializers.Serializer):

    @classmethod
    def adjust(cls, snapshot_model: Type[models.AbstractSnapshot]):
        assert issubclass(snapshot_model, models.AbstractSnapshot)
        options = snapshot_model.get_options()
        attrs = {}
        for field in options.fields:
            attrs[field] = serializers.IntegerField(source=f'{options.name}_{field}', required=False)
        return type('SnapshotSerializer', (cls,), attrs)


class FacultySerializer(BaseRatingSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    university_id = serializers.IntegerField()


class DepartmentSerializer(BaseRatingSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    faculty_id = serializers.IntegerField()


class PersonSerializer(BaseRatingSerializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    department_id = serializers.IntegerField()
    person_type_ids = serializers.SerializerMethodField()

    def get_person_type_ids(self, instance):
        return instance.person_types.all().values_list('id', flat=True)


class BaseRatingOptionsSerializer(serializers.Serializer):
    SCOPUS = 'scopus'
    GOOGLE_SCHOLAR = 'google-scholar'
    SEMANTIC_SCHOLAR = 'semantic-scholar'
    WOS = 'wos'
    REVISION_TYPES = (SCOPUS, GOOGLE_SCHOLAR, SEMANTIC_SCHOLAR, WOS)

    revision_id = serializers.IntegerField(required=False)
    revision_type = serializers.ChoiceField(choices=REVISION_TYPES)


class PersonRatingOptionsSerializer(BaseRatingOptionsSerializer):
    university_id = serializers.IntegerField()
    person_type_ids = serializers.ListField(child=serializers.IntegerField(), required=False)


class FacultyRatingOptionsSerializer(BaseRatingOptionsSerializer):
    university_id = serializers.IntegerField()


class DepartmentRatingOptionsSerializer(BaseRatingOptionsSerializer):
    faculty_id = serializers.IntegerField()
