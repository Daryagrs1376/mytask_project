from rest_framework import viewsets, permissions # پرمیشن برای اینکه بدونم چه کسی به ویوست دسترسی داره
from .models import Ticket, Message, Profile
from .serializers import TicketSerializer, MessageSerializer, ProfileSerializer  #سریالایزرهایی که به مدلها وصل میشن
from rest_framework.exceptions import PermissionDenied #برای خطای پرمیشن  یعنی اگر کاربر دسترسی نداشت خطا بده
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OTP
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.authtoken.models import Token




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
        user = request.user 

        if user.is_staff:
            role = user.adminprofile.role
            if role != 'manager':
                raise PermissionDenied("Don't allow deleting messages")
            
        else:
            Message = self.get_object()
            if Message.sender != user:
                raise PermissionDenied("You  don't have permission to delete this message") 
                
        return super().destroy(request, *args, **kwargs) # اگر کاربر استف نباشه پیامش حذف میشه
  

class RequestOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'ایمیل الزامی است.'}, status=400)

        otp = OTP.objects.create(email=email)
        print(f"کد OTP برای {email} => {otp.code}")
        return Response({'message': 'کد OTP ارسال شد (در کنسول قابل مشاهده است).'})
    

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            otp = OTP.objects.filter(email=email).latest('created_at')
        except OTP.DoesNotExist:
            return Response({'error': 'کدی برای این ایمیل یافت نشد.'}, status=400)

        if otp.code != code:
            return Response({'error': 'کد اشتباه است.'}, status=400)

        user, created = User.objects.get_or_create(username=email, email=email)
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
    
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # فقط پروفایل خود کاربر را برگرداند
        return Profile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        # هنگام آپدیت کردن، اطمینان حاصل شود که فقط روی پروفایل خودش کار می‌کند
        serializer.save(user=self.request.user)

    def perform_create(self, serializer):
        # معمولاً در این ViewSet ایجاد نمی‌کنی ولی برای اطمینان
        serializer.save(user=self.request.user)