from rest_framework import serializers


class ArticleSerializer(serializers.Serializer):

    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField(allow_null=True)
    scopus = serializers.BooleanField(default=False)
    google_scholar = serializers.BooleanField(default=False)
    semantic_scholar = serializers.BooleanField(default=False)
    wos = serializers.BooleanField(default=False)

    def get_id(self, instance):
        return instance.article.id

    def get_title(self, instance):
        return instance.article.title

    def get_year(self, instance):
        return instance.article.year
