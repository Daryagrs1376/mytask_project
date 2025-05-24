from django.db import models 
from django.contrib.auth.models import User 
import random


#مدل سازمان
class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True) 
    users = models.ManyToManyField(User, related_name='organizations') 
                                    #با این میخوام از یوزر سازمان هاش را صدا بزنم
    def __str__(self): # متدی برای نمایش خوانایی
        return self.name  #برای نمایش نام سازمان در ادمین
    


class Ticket(models.Model):
    title = models.CharField(max_length=255) 
    description = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')], default='open') 

    def __str__(self):
        return self.title 


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='messages', on_delete=models.CASCADE) 
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField() # متن پیام 
    created_at = models.DateTimeField(auto_now_add=True) 
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True) 
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)  
    # از CASCADE استفاده کردم که وقتی کاربر حذف شد تیکت هاشم پاک بشه ولی طبق داکیومنت اگر کامنت ها را بخوام نگهدارم از set-null استفاده میکنم 


    def __str__(self):
        return f"Message from {self.sender.username} for {self.ticket.title}"
                                    #نمایش پیام: فرستنده + عنوان تیکت 


# نقش کاربر در سازمان/ برای نقش های عمومی / کاربران غیر ادمین 
class Role(models.Model):
    name = models.CharField(max_length=100, choices=[
        ('viewer', 'Viewer'), # بیننده 
        ('responder', 'Responder'), #پاسخگو
        ('manager', 'Manager')
    ]) 
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE) # نقش سازمان اگر سازمان حذف بشه نقش هم حذف بشه
    users = models.ManyToManyField(User) # ارتباط چند به چند بین کاربران و نقش‌ها
# اینجا میخوام بگم که یک کاربر میتونه چند نقش داشته باشه و یک نقش هم میتونه چندکاربر داشته باشه
    
    def __str__(self): 
        return self.name 


class AdminProfile(models.Model):
    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('responder', 'Responder'),
        ('manager', 'Manager'),
    ] 

    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer') 
                                            # در صورت حذف ادمین پروفایلش هم حذف بشه
    
    def __str__(self):
        return f"{self.user.username} ({self.role})" 


class OTP(models.Model):
    email = models.EmailField() 
    code = models.CharField(max_length=6) 
    created_at = models.DateTimeField(auto_now_add=True) 

    def save(self, *args, **kwargs): # برای اینکه کد تصادفی ایجاد کنم اگر کدی وجود نداشته باشه
        if not self.code: 
            self.code = str(random.randint(100000, 999999)) 
        super().save(*args, **kwargs) 



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=100, blank=True) 
    phone = models.CharField(max_length=20, blank=True) 
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True) 