from rest_framework import serializers
from rest_framework.response import Response

from product.models import Product, Category, ProductBookMark, ProductRating


class CategorySerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time', 'child']

    def get_child(self, obj):
        query = Category.objects.filter(parent=obj.id)
        serializer = CategorySerializer(query,many=True)
        # return CategorySetializer(obj.(related_name).all).data()
        return serializer.data

class ProductSerializer(serializers.ModelSerializer):
    categurise = CategorySerializer(many=True)
    user_rate = serializers.SerializerMethodField()
    user_bookmark = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'categurise', 'rating_avg', 'rating_count', 'user_rate',
                  'user_bookmark']

    def get_user_rate(self, obj):
        request = self.context['request']
        user = request.user
        if user and user.is_authenticated:
            try:
                rate = ProductRating.objects.get(user=user, product=obj).rate
            except ProductRating.DoesNotExist:
                pass
            else:
                return rate

    def get_user_bookmark(self, obj):
        request = self.context['request']
        user = request.user
        if user and user.is_authenticated:
            try:
                bookmark = ProductBookMark.objects.get(user=user, product=obj).like_status
            except ProductBookMark.DoesNotExist:
                pass
            else:
                return bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    like_status = serializers.BooleanField(required=True)

    class Meta:
        model = ProductBookMark
        fields = ['like_status', ]

    def create(self, validated_data):
        like_status = {'like_status': validated_data.pop('like_status', False)}
        instance, _created = ProductBookMark.objects.update_or_create(
            **validated_data,
            defaults=like_status
        )
        return instance


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['rate', 'user', 'product']
        read_only_fields = ['user', 'product']

    def create(self, validated_data):
        rate = {'rate': validated_data.pop('rate')}
        instance, _created = ProductRating.objects.update_or_create(
            **validated_data,
            defaults=rate
        )
        return instance
