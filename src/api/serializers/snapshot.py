from typing import Type
from rest_framework import serializers
from core import models


class RevisionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)


class BaseSnapshotSerializer(serializers.Serializer):

    revision = RevisionSerializer()
    person_id = serializers.IntegerField()

    @classmethod
    def adjust(cls, snapshot_model: Type[models.AbstractSnapshot]):
        assert issubclass(snapshot_model, models.AbstractSnapshot)
        options = snapshot_model.get_options()
        attrs = {}
        for field in options.fields:
            attrs[field] = serializers.IntegerField()
        return type('SnapshotSerializer', (cls,), attrs)
