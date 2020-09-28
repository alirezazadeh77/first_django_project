from rest_framework import serializers
from rest_framework.exceptions import ParseError

from commenting.models import ProductComment


class CommentingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['id', 'product', 'user', 'content']
        read_only_fields = ['id', 'product', 'user']

    def validate(self, attrs):
        content = attrs['content']
        if "test" in content:
            raise ParseError({"Error": "test can not be in content"})
