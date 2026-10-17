from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessProfileViewSet, ProductViewSet, ChatBotViewSet

router = DefaultRouter()
router.register(r'businesses', BusinessProfileViewSet)
router.register(r'products', ProductViewSet)
router.register(r'chat', ChatBotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]