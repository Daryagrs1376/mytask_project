from django.urls import path, include
from rest_framework.routers import DefaultRouter # از DefaultRouter برای ساخت خودکار urls ها استفاده میکنم
from .views import TicketViewSet, MessageViewSet # از ویو ست های مسیج و تیکت استفاده میکنم



router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket') 
router.register(r'messages', MessageViewSet, basename='message') 


urlpatterns = [
    path('', include(router.urls)),
]
