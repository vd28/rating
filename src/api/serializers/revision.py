from rest_framework import serializers


class RevisionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
