from datetime import datetime

from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncDate
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated

from .models import Post, Like, User
from .serializers import PostSerializer, LikeSerializer, AnalyticsSerializer
from .permissions import IsOwnerOrSuperuser


class PostListView(ListAPIView):
    """
        List all posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UsersPostsListView(ListAPIView):
    """
        List all posts that created specific user.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        posts = Post.objects.filter(creator=user)
        return posts


class PostCreateView(CreateAPIView):
    """
        Create new post.

        Authorization required.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer


class PostDeleteView(DestroyAPIView):
    """
        Delete post.

        Authorization required. Need to be creator of post or superuser.
    """
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrSuperuser, )


class LikeCreateView(CreateAPIView):
    """
        Add like to post.
        If user already added like to this post, then it removing like and
         returning status 204 and {"detail": "Like removed"}.

        Authorization required.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeSerializer


class AnalyticsView(GenericAPIView):
    """
        Analytics about number likes per day. If date_from or date_to not provided it would filter by datetime.min/max.
    """

    def get(self, request):
        serializer = AnalyticsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        date_from = data.get('date_from')
        date_to = data.get('date_to')

        like_analytics = list(
            Like.objects.filter(creation_date__gte=date_from if date_from else datetime.min,
                                creation_date__lte=date_to if date_to else datetime.max)
            .annotate(date=TruncDate('creation_date'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
            .values('date', 'count')
        )

        return Response(like_analytics, status=200)


class UserActivityView(GenericAPIView):
    """
        Provide activity info about user.
    """

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response("User with this username does not exists", status=404)
        return Response({"last_login": user.last_login, "last_request": user.last_request}, status=200)
