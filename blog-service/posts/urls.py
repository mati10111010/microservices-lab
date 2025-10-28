from django.contrib import admin
from django.urls import path, include
from .views import (
    PostListAPIView,
    HealthCheckAPIView
)
urlpatterns = [
    path('health/', HealthCheckAPIView.as_view(), name='health-check'), # <--- Nuevo
    path('posts/', PostListAPIView.as_view(), name='post-list'),
]