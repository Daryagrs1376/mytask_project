from django.db.models.signals import post_save # برای سیگنال زدن و سیو کردن پست استفاده میشه بعد از سیو شدن یک آبجکت اجرا میشه 
from django.dispatch import receiver # برای دریافت سیگنال استفاده میکنم
from django.contrib.auth.models import User #برای مدل یوزر 
from .models import AdminProfile #میخوام وقتی یک کاربر جدید ساخته شد یک پروفایل براش بسازم
from .models import Profile



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User) # این یک دستور مخصوص دکوراتور در جنگو است که میگه وقتی یک یوزر جدید ساخته شد تابع زیر را اجرا کن
def create_admin_profile(sender, instance, created, **kwargs): #میگم که مدل یوزر را بفرست و اگر  کاربر جدید ساخته شد این تابع را اجرا کن/instanceبرای یوزر که ذخیره شده/createdبرای ساخت یوزر جدیده/kwargsبرای مقدارهای اضافی ک جنگو میفرسته یعنی زمانیکه میخوام فیلدها اپدیت بشه 
    if created and instance.is_staff: # وقتی یوزر جدید ساخته باشه is staff = true باشه یعنی ادمین
        AdminProfile.objects.create(user=instance, organization_id=1) # میخوام یک پروفایل ادمین براش بسازم و سازمانش 1 باشه

### این فایل برای این ساختم که وقتی یک کاربر جدید ساخته میشه و اگر استف باشه یک پروفایل ادمین براش ساخته بشه و سازمانش 1 باشه ###
### در مدل پیش‌فرض User در جنگو، یک فیلد به نام is_staff وجود دارد که اگر مقدارش True باشد یعنی این کاربر اجازه دارد وارد پنل ادمین جنگو شود ###  