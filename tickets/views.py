from rest_framework import viewsets, permissions
from .models import Ticket, Message
from .serializers import TicketSerializer, MessageSerializer
from rest_framework.exceptions import PermissionDenied



class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
        
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(sender=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            role = user.adminprofile.role
            if role not in ['responder', 'manager']:
                raise PermissionDenied("don't allow to send messages")
        serializer.save(sender=user)