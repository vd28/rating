from typing import Type

from rest_framework import serializers

from core import models
from api.common import SNAPSHOT_MODEL_MAPPING


class BaseRatingSerializer(serializers.Serializer):

    @classmethod
    def adjust(cls, snapshot_model: Type[models.AbstractSnapshot]):
        assert issubclass(snapshot_model, models.AbstractSnapshot)
        options = snapshot_model.get_options()
        attrs = {}
        for field in options.fields:
            attrs[field] = serializers.IntegerField(source=f'{options.name}_{field}', required=False)
        return type('RatingSerializer', (cls,), attrs)


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
    revision_id = serializers.IntegerField(required=False)
    snapshot = serializers.ChoiceField(choices=tuple(SNAPSHOT_MODEL_MAPPING.keys()))


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
