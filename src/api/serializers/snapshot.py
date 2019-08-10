from typing import Type

from rest_framework import serializers

from core import models
from .revision import RevisionSerializer


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
