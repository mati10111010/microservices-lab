from django.contrib import admin
from django.urls import path, include
from .views import (
    PostListAPIView,
    HealthCheckAPIView,
    CategoryListAPIView
)
urlpatterns = [
    path('health/', HealthCheckAPIView.as_view(), name='health-check'),
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
]