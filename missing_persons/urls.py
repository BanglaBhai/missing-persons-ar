from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MissingPersonViewSet

router = DefaultRouter()
router.register(r'persons', MissingPersonViewSet, basename='missing-person')

urlpatterns = [
    path('', include(router.urls)),
]