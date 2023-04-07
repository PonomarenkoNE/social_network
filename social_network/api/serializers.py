from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Post, Like


class RaiseDeleteStatus(APIException):
    status_code = HTTP_204_NO_CONTENT


class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    creator = serializers.SlugRelatedField('username', read_only=True)
    creation_date = serializers.DateTimeField(read_only=True)
    like_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        post = Post.objects.create(**validated_data)
        return post

    def get_like_count(self, obj):
        return obj.count_likes()

    def get_user_liked(self, obj):
        user = self.context['request'].user
        if Like.objects.filter(to_post=obj, creator=user).exists():
            return True
        return False

    class Meta:
        model = Post
        fields = ('id', 'creator', 'creation_date', 'like_count', 'user_liked', 'title', 'content')


class LikeSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(read_only=True)
    creator = serializers.SlugRelatedField('username', read_only=True)

    class Meta:
        model = Like
        fields = ('to_post', 'creator', 'creation_date')

    def validate_to_post(self, value):
        user = self.context['request'].user
        unlike = Like.objects.filter(to_post=value, creator=user).first()
        if unlike is not None:
            unlike.delete()
            raise RaiseDeleteStatus(detail="Like removed", code=204)
        return value

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        like = Like.objects.create(**validated_data)
        return like


class AnalyticsSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False)
    date_ro = serializers.DateField(required=False)
