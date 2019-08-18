from rest_framework import serializers
import pytz


class RevisionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True, default_timezone=pytz.utc)
