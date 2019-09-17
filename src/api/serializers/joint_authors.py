from rest_framework import serializers


class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    articles_count = serializers.IntegerField(required=False)


class JointAuthorsSerializer(serializers.Serializer):
    self = PersonSerializer()
    joint_authors = serializers.ListField(child=PersonSerializer())
