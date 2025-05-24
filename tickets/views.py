from rest_framework import viewsets, permissions, status
from .models import Ticket, Message, Profile, OTP
from rest_framework.exceptions import PermissionDenied 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from .serializers import(
    RequestOTPSerializer,
    VerifyOTPSerializer,
    ProfileSerializer,
    MessageSerializer,
    TicketSerializer
)



class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer 
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self): 
        user = self.request.user

        if user.is_staff:
        
            return Ticket.objects.all()
        # کاربر عادی: فقط تیکت‌های خودش
        return Ticket.objects.filter(user=user)

    def perform_create(self, serializer): 

        serializer.save(user=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user 
        # اگر کاربر ادمین بود همه پیام ها برگرده
        if user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(sender=user)  

    # هنگام post اطلاعات کاربر لاگین شده را بگیریم
    def perform_create(self, serializer):
        user = self.request.user 

        if user.is_staff:
            role = user.adminprofile.role 
            if role not in ['responder', 'manager']: 
                raise PermissionDenied("Don't allow answer messages") 
        serializer.save(sender=user) 


    def destroy(self, request, *args, **kwargs): 
        user = request.user  

        if user.is_staff: 
            role = user.adminprofile.role 
            if role != 'manager': 
                raise PermissionDenied("Don't allow deleting messages") 
            
        else: 
            Message = self.get_object()  
            if Message.sender != user: # اگر کاربر لاگین شده فرستنده پیام نباشه
                
                raise PermissionDenied("You  don't have permission to delete this message") 
                
        return super().destroy(request, *args, **kwargs) # اگر کاربر استف نباشه پیامش حذف میشه
  

class RequestOTPViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = OTP.objects.create(email=email)
        print(f"OTP برای {email}: {otp.code}")
        return Response({'message': 'کد ارسال شد (در کنسول قابل مشاهده است)'})
    

class VerifyOTPViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            otp = OTP.objects.filter(email=email).latest('created_at')

        except OTP.DoesNotExist:
            return Response({'error': 'کدی برای این ایمیل یافت نشد'}, status=400)
        

        if otp.code != code:
            return Response({'error': 'کد اشتباه است'}, status=400)

        user, _ = User.objects.get_or_create(username=email, email=email)

        login(request, user)

        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({'token': token.key})
    

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)