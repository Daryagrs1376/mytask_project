from django.urls import path, include
from rest_framework.routers import DefaultRouter # از DefaultRouter برای ساخت خودکار urls ها استفاده میکنم
from .views import TicketViewSet, MessageViewSet, RequestOTPView, VerifyOTPView, ProfileViewSet # از ویو ست های مسیج و تیکت استفاده میکنم



router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket') 
router.register(r'messages', MessageViewSet, basename='message') 
router.register(r'profile', ProfileViewSet, basename='profile')


urlpatterns = [
    path('request-otp/', RequestOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('', include(router.urls)),
]
