from django.core.management.base import BaseCommand
from faker import Faker
from tickets.models import Ticket, Message
from django.contrib.auth.models import User
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with fake tickets and messages'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding tickets...")

        # ایجاد چند کاربر تستی
        for i in range(3):
            username = f"user{i}"
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password='1234')

        users = list(User.objects.all())

        # تولید تیکت و پیام
        for _ in range(10):  # 10 تیکت
            user = random.choice(users)
            ticket = Ticket.objects.create(
                title=fake.sentence(),
                description=fake.paragraph(),
                user=user,
                status=random.choice(['open', 'closed']),
            )

            # پیام‌های هر تیکت
            for _ in range(random.randint(1, 5)):
                Message.objects.create(
                    ticket=ticket,
                    sender=random.choice(users),
                    content=fake.paragraph(),
                )

        self.stdout.write(self.style.SUCCESS("✅ Tickets and messages seeded successfully!"))
