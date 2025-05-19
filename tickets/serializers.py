from rest_framework import serializers
from .models import Ticket, Message # مدل تیکت و مسج از فایل مدل ها ایمپورت میشه



class MessageSerializer(serializers.ModelSerializer): # از مدل سریالایزر ارث بری میکنه و بطور خودکار فیلدهای مدل مسج را به api تبدیل میکنه 
    sender = serializers.StringRelatedField(read_only=True) # فرستنده پیام بصورت رشته ای نشان میدهد و فقط خواندی است و زمان متد put و post نباید باشه 
    replies = serializers.SerializerMethodField() 

    class Meta:
        model = Message # میخوام بگم این سریالایزر برای مدل مسیج است
        fields = ['id', 'ticket', 'sender', 'content', 'created_at', 'attachment', 'parent', 'replies'] # فیلدهای خروجی json
        extra_kwargs = {
            'ticket': {'write_only': True},
            'parent': {'write_only': True}

        } # هنگام ارسال پیام استفاده میشه متد post / هنگام ارسال پیام لازم اما در خروجی نشان داده نمیشه


    def validate_attachment(self, value): # برای اعتبارسنجی فیلد از attachment استفاده میشه 
        # برای اندازه فایل
        if value:
            max_size = 10 * 1024 * 1024  # اگر فایل ارسال شده باشه حجمش بیشتر از 10 مگ باشه یک validationeror برمیگردونه ولی اگر اکی بود مفدار را برگردونه
            if value.size > max_size:
                raise serializers.ValidationError("حجم فایل  تا سقف 10 مگابایت")
        return value
    

# متد رپلای پیام
    def get_replies(self, obj):

        if obj.replies.exists(): # اگر رپلای هایی وجود داشته باشد سریالایزر انها را برمیگردونه 
            return MessageSerializer(obj.replies.all(), many=True, context=self.context).data
        return [] # اگر رپلای وجود نداشته باشه سریالایزر انها را خالی برمیگردونه
    


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) #پیام بصورت رشته اس و فقط خواندنی است و متد put و post نباید باشه 
    messages = MessageSerializer(many=True, read_only=True) # پیام های تیکت را نشان میده و فقط در خروجی نمایش داده میشه ن در زمان ایجاد یا ویرایش تیکت 


    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'created_at', 'status', 'user', 'messages'] #فیلدهای خروجی json
