from rest_framework import viewsets, permissions # پرمیشن برای اینکه بدونم چه کسی به ویوست دسترسی داره
from .models import Ticket, Message
from .serializers import TicketSerializer, MessageSerializer #سریالایزرهایی که به مدلها وصل میشن
from rest_framework.exceptions import PermissionDenied #برای خطای پرمیشن  یعنی اگر کاربر دسترسی نداشت خطا بده




class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer # سریالایزر اصلی این ویو تیکت سریالایزره
    permission_classes = [permissions.IsAuthenticated] # فقط کاربرانی که لاگین کردن به این ویو دسترسی دارن


    def get_queryset(self): # در کلاس های مدل ویو ست داخل جنگو این متد مشخص میکنه که چه داده هایی را برمیگردونه
        # اگر کاربر ادمین بود همه تیکت ها برگرده اگر  ادمین نبود فقط تیکت های خودش برگرده
        user = self.request.user
        if user.is_staff:
        
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)


    def perform_create(self, serializer): #این متد سفارشی از کلاس modelviewset هست هر وقت در api عملیات post انجام بشه این متد صدا زده میشه 
        serializer.save(user=self.request.user) #اگر کاربر عادی بخواد یک تیکت ثبت کنه لازم نیست توی post بگه user کیه



class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(sender=user)

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_staff:
            role = user.adminprofile.role
            if role not in ['responder', 'manager']:
                raise PermissionDenied("Don't allow answer messages")
        serializer.save(sender=user)

# از این متد استفاده کردم که ویوست سفارشی را قبل از حذف کردن بررسی کنیم که کاربر مجاز به حذف هست یا ن
    def destroy(self, request, *args, **kwargs): # destroyبرای حذف استفاده میشه / selfاز این متد به بقیه متدها دسترسی داریم/  requestشامل تمام اطلاعات http/ *argsیک سینتکس  پایتونیه 
        user = request.user 

        if user.is_staff:
            role = user.adminprofile.role
            if role != 'manager':
                raise PermissionDenied("Don't allow deleting messages")
        return super().destroy(request, *args, **kwargs)
        