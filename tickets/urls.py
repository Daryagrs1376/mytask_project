from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import (
    TicketViewSet,
    MessageViewSet,
    RequestOTPView,
    VerifyOTPView,
    ProfileViewSet,
    RequestOTPViewSet,
    VerifyOTPViewSet
)



router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'messages', MessageViewSet, basename='message') 
router.register(r'request-otp', RequestOTPViewSet, basename='request-otp')
router.register(r'verify-otp', VerifyOTPViewSet, basename='verify-otp')
router.register(r'profile', ProfileViewSet, basename='profile')


urlpatterns = [
    path('', include(router.urls)),
]
