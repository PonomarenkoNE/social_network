from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view()),
    path('posts/<str:username>/', views.UsersPostsListView.as_view()),
    path('posts/create', views.PostCreateView.as_view()),
    path('posts/<int:pk>/delete', views.PostDeleteView.as_view()),
    path('like/', views.LikeCreateView.as_view()),
    path('analytics/', views.AnalyticsView.as_view()),
    path('user-activity/<str:username>/', views.UserActivityView.as_view())
]