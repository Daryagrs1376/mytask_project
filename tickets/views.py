from rest_framework import viewsets, permissions, status # پرمیشن برای اینکه بدونم چه کسی به ویوست دسترسی داره
from .models import Ticket, Message, EmailOTP
from .serializers import TicketSerializer, MessageSerializer, SendOTPSerializer #سریالایزرهایی که به مدلها وصل میشن
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone
import random
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils.timezone import now
from .models import UserProfile



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
    

class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        code = str(random.randint(100000, 999999))

        EmailOTP.objects.update_or_create(
            email=email,
            defaults={
                'code': code,
                'created_at': timezone.now(),
                'is_verified': False
            }
        )

        print(f"کد OTP برای {email}: {code}")  

        return Response({'message': 'کد OTP ارسال شد'}, status=status.HTTP_200_OK)
    

class VerifyOTPView(APIView):
    def post (self, request):
        email, code = request.data.get('email'), request.data.get('code')
        if not all([email, code]):
            return Response({'error': 'ایمیل و کد را وارد کنید'}, status=400)
        
        otp = EmailOTP.objects.filter(email=email, code=code).first()
        if not otp or  (now() - otp.created_at).total_seconds() > 300:
            return Response({'error': 'کد نادرست است یا منقضی شده'}, status=400)
        
        otp.is_verified = True
        otp.save()

        user, _ = User.objects.get_or_create(username=email, defaults={'email': email})
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'message': 'ورود موفق', 'token': token.key})
    


class OTPVerifyView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        # فرض: OTP را از مدل ذخیره کرده‌ایم و حالا بررسی می‌کنیم
        if otp == "1234":  # برای تست، فرض کردیم otp صحیحه
            user, created = User.objects.get_or_create(username=email, email=email)

            # اگر کاربر تازه ساخته شده، پروفایل هم بساز
            if created:
                UserProfile.objects.create(user=user)

            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)