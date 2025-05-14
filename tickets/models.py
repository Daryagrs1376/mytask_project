from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name='organizations')
    
    def __str__(self):
        return self.name
    

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
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True) # برای ذخیره فایل ها 10 گیگ
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)  #برای قابل رپلای شدن پیام


    def __str__(self):
        return f"Message from {self.sender.username} for {self.ticket.title}"


class Role(models.Model):
    name = models.CharField(max_length=100, choices=[
        ('viewer', 'Viewer'),
        ('responder', 'Responder'),
        ('manager', 'Manager')
    ])
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    
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

    def __str__(self):
        return f"{self.user.username} ({self.role})"
