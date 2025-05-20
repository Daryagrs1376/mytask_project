from rest_framework import viewsets, permissions # پرمیشن برای اینکه بدونم چه کسی به ویوست دسترسی داره
from .models import Ticket, Message
from .serializers import TicketSerializer, MessageSerializer #سریالایزرهایی که به مدلها وصل میشن
from rest_framework.exceptions import PermissionDenied #برای خطای پرمیشن  یعنی اگر کاربر دسترسی نداشت خطا بده
from django.shortcuts import get_object_or_404




class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer # سریالایزر اصلی این ویو تیکت سریالایزره
    permission_classes = [permissions.IsAuthenticated] # فقط کاربرانی که لاگین کردن به این ویو دسترسی دارن


    def get_queryset(self): 
        user = self.request.user
        if user.is_staff:
        
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)


    def perform_create(self, serializer): #این متد سفارشی از کلاس modelviewset هست هر وقت در api عملیات post انجام بشه این متد صدا زده میشه 
        serializer.save(user=self.request.user) #اگر کاربر عادی بخواد یک تیکت ثبت کنه لازم نیست توی post بگه user کیه



class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated] # پرمیشن برای اینه که فقط کاربرانی که لاگین کردن به این ویو دسترسی دارن


    
    # اگر کاربر عادی باشه فقط پیام های خودش برگرده و بقیه اطلاعات را نتونه ببینه 

    def get_queryset(self):
        user = self.request.user 
        if user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(sender=user) 


    # برای اینکه پاسخ بده و ببینه

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff and getattr(getattr(user, 'adminprofile', None), 'role', None) == 'responder':
            raise PermissionDenied("Responder can only reply to tickets.") 
        serializer.save(sender=user)    

            


    def destroy(self, request, *args, **kwargs):
        user = request.user

        if user.is_staff and user.adminprofile.role == 'manager':
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response (status=status.HTTP_204_NO_CONTENT)
    



        
        
    # def perform_create(self, serializer):
    #     role = getattr(getattr(self.request.user, 'adminprofile', None), 'role', None)
    #     user = self.request.user 

    #     if user.is_staff and role == 'responder': 
    #         if not serializer.validated_data.get("parent"):
    #             raise PermissionDenied("Responder allowed to answer only.")