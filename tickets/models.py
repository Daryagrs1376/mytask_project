from django.db import models # مدلهای جدول پایگاه داده 
from django.contrib.auth.models import User # مدل پیش فرض کاربر یوزر



#مدل سازمان
class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True) # نام سازمان از نوع رشته طول 255 مقدار ثابت 
    users = models.ManyToManyField(User, related_name='organizations') # منی تو منی برای این گذاشتم که رابطه چند به چند بین سازمان و کاربران باشه
                                    #با این میخوام از یوزر سازمان هاش را صدا بزنم
    def __str__(self): # متدی برای نمایش خوانایی
        return self.name  #برای نمایش نام سازمان در ادمین
    


class Ticket(models.Model):
    title = models.CharField(max_length=255) # عنوان تیکت از نوع رشته با طول 255
    description = models.TextField() #توضیح تیکت تکست فیلد  اندازه اش محدود نیست
    created_at = models.DateTimeField(auto_now_add=True) #زمان ساخت تیکت #هنگام ساخت زمان بطور خودکار ثبت بشه
    updated_at = models.DateTimeField(auto_now=True) #auto now = هر بار تیکت ذخیره میشه این فیلد به روز بشه 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets') #کاربر سازنده تیکت #اگر کاربر حذف بشه تیکت هاشم حذف بشه
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')], default='open') # علت استفادم از choice چون جلوی اشتباهات را میگیره چون خودم مقدار مشخص براش ثبت کردم 

    def __str__(self):
        return self.title 


# مدل برای پیام های تیکت برای دخیره پیامهای تیکت استفاده میشه
class Message(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='messages', on_delete=models.CASCADE) 
    sender = models.ForeignKey(User, on_delete=models.CASCADE) # ارسال کننده پیام از مدل یوزر 
    content = models.TextField() # متن پیام 
    created_at = models.DateTimeField(auto_now_add=True) # زمان ارسال پیام # زمان  بروز رسانی پیام
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True) # برای ذخیره فایل ها 10 گیگ
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)  # برای اضافه کردن قابلیت رپلای پیام
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
    ]) # نقش ها یکی از این 3 مقدار باشه 
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE) # نقش سازمان اگر سازمان حذف بشه نقش هم حذف بشه
    users = models.ManyToManyField(User) # ارتباط چند به چند بین کاربران و نقش‌ها
# اینجا میخوام بگم که یک کاربر میتونه چند نقش داشته باشه و یک نقش هم میتونه چندکاربر داشته باشه
    
    def __str__(self):
        return self.name # میخوام نام نقش داخل ادمین نمایش بدم


# کاربرانی هستن که نقش مهم در سازمان دارن / کاربران دارای پروفایل در سازمان 
class AdminProfile(models.Model):
    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('responder', 'Responder'),
        ('manager', 'Manager'),
    ] # تعریف نقش برای ادمین

    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}) # رابطه یک به یک با کاربرانی که ادمین هستن #لیمیتد چویس برای محدود کردن انتخاب ادمینها
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE) # مشخص کردن ادمین برای کدام سازمان است
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer') # نقش ادمین در سازمان
                                            # در صورت حذف ادمین پروفایلش هم حذف بشه
    
    def __str__(self):
        return f"{self.user.username} ({self.role})" # نمایش نام ادمین و نقش ادمین



class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.code}"
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.email