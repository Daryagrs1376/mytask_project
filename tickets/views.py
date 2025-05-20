from rest_framework import viewsets, permissions # پرمیشن برای اینکه بدونم چه کسی به ویوست دسترسی داره
from .models import Ticket, Message
from .serializers import TicketSerializer, MessageSerializer #سریالایزرهایی که به مدلها وصل میشن
from rest_framework.exceptions import PermissionDenied #برای خطای پرمیشن  یعنی اگر کاربر دسترسی نداشت خطا بده
from django.shortcuts import get_object_or_404




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
    permission_classes = [permissions.IsAuthenticated] # پرمیشن برای اینه که فقط کاربرانی که لاگین کردن به این ویو دسترسی دارن
    # اینجا میخوام بگم اگر کاربر ادمین بود همه پیام ها را ببینه و اگر عادی بود فقط پیام های خودش را ببینه

    def get_queryset(self):
        user = self.request.user # با ریکوست دادن اطلاعات یوزر را میگیرم
        # اگر کاربر ادمین بود همه پیام ها برگرده
        if user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(sender=user) # اگر کاربر عادی باشه فقط پیام های خودش برگرده و بقیه اطلاعات را نتونه ببینه 

    # هنگام post اطلاعات کاربر لاگین شده را بگیریم
    def perform_create(self, serializer):
        user = self.request.user

        if user.is_staff:
            role = user.adminprofile.role
            if role not in ['responder', 'manager']:
                raise PermissionDenied("Don't allow answer messages")
        serializer.save(sender=user)

# از این متد استفاده کردم که ویوست سفارشی را قبل از حذف کردن بررسی کنیم که کاربر مجاز به حذف هست یا ن
    def destroy(self, request, *args, **kwargs): # destroyبرای حذف استفاده میشه / selfاز این متد به بقیه متدها دسترسی داریم/  requestشامل تمام اطلاعات http/ *argsیک سینتکس  پایتونیه 
        user = request.user # اینجا یوزر لاگین شده را میبینم که اجازه حذف داره یا ن
        Message = get_object_or_404(Message, pk=kwargs["pk"]) # با این متد میخوام پیام را بگیرم اگر وجود نداشت خطا بده


        if user.is_staff: # کاربر ادمین هست
            # اگر کاربر ادمین بود و نقشش مدیر بود اجازه حذف پیام داره
            role = user.adminprofile.role
            if role != 'manager': # فقط مدیر 
                raise PermissionDenied("You don't have permission to delete messages.")
            
        else: # اگر کاربر عادی بود
                                        
            if Message.sender != user: # اگر پیام برای خودش بود حذف کنه
                raise PermissionDenied("You  don't have permission to delete this message") 
                
        return super().destroy(request, *args, **kwargs) # اگر کاربر استف نباشه پیامش حذف میشه
  