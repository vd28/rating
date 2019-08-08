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
        return type('RatingSerializer', (cls,), attrs)


class BaseSnapshotSerializer(serializers.Serializer):

    @classmethod
    def adjust(cls, snapshot_model: Type[models.AbstractSnapshot]):
        assert issubclass(snapshot_model, models.AbstractSnapshot)
        options = snapshot_model.get_options()
        attrs = {}
        for field in options.fields:
            attrs[field] = serializers.IntegerField()
        return type('SnapshotSerializer', (cls,), attrs)
