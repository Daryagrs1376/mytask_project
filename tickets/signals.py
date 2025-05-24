from django.db.models.signals import post_save 
from django.dispatch import receiver 
from django.contrib.auth.models import User 
from .models import AdminProfile 
from .models import Profile



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User) 
def create_admin_profile(sender, instance, created, **kwargs): #میگم که مدل یوزر را بفرست و اگر  کاربر جدید ساخته شد این تابع را اجرا کن/instanceبرای یوزر که ذخیره شده/createdبرای ساخت یوزر جدیده/kwargsبرای مقدارهای اضافی ک جنگو میفرسته یعنی زمانیکه میخوام فیلدها اپدیت بشه 
    if created and instance.is_staff: # وقتی یوزر جدید ساخته باشه is staff = true باشه یعنی ادمین
        AdminProfile.objects.create(user=instance, organization_id=1)

### این فایل برای این ساختم که وقتی یک کاربر جدید ساخته میشه و اگر استف باشه یک پروفایل ادمین براش ساخته بشه و سازمانش 1 باشه ###
