from rest_framework import serializers
from .models import Ticket, Message



class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'ticket', 'sender', 'content', 'created_at', 'attachment', 'parent', 'replies']
        extra_kwargs = {
            'ticket': {'write_only': True},
            'parent': {'write_only': True}

        }


    def validate_attachment(self, value):
        # برای اندازه فایل
        if value:
            max_size = 10 * 1024 * 1024  # 10 مگابایت
            if value.size > max_size:
                raise serializers.ValidationError("حجم فایل  تا سقف 10 مگابایت")
        return value
    
# قابلیت رپلای پیام
    def get_replies(self, obj):

        if obj.replies.exists():
            return MessageSerializer(obj.replies.all(), many=True, context=self.context).data
        return []
    

class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'created_at', 'status', 'user', 'messages']
