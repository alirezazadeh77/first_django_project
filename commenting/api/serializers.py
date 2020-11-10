from rest_framework import serializers
from rest_framework.exceptions import ParseError

from commenting.models import ProductComment, CommentVote


class CommentingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['id', 'product', 'user', 'content', 'positive_votes', 'negative_votes']
        read_only_fields = ['id', 'product', 'user', 'positive_votes', 'negative_votes']

    def validate(self, attrs):
        content = attrs['content']
        if "test" in content:
            raise ParseError({"Error": "test can not be in content"})


class VoteSerializer(serializers.ModelSerializer):
    comment = CommentingSerializer(read_only=True)

    class Meta:
        model = CommentVote
        fields = ['vote', 'user', 'comment']
        read_only_fields = ['user', ]

    def create(self, validated_data):
        vote = {
            'vote': validated_data.pop('vote')
        }
        instance, _created = self.Meta.model.objects.update_or_create(
            **validated_data,
            defaults=vote
        )
        return instance
