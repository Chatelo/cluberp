from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from bar.models import Drink

class Command(BaseCommand):
    help = 'Checks stock levels and sends notifications for low stock.'

    def handle(self, *args, **options):
        low_stock_threshold = 10  # Define your desired threshold here
        drinks = Drink.objects.filter(stock_level__lte=low_stock_threshold)
        if drinks:
            message = 'The following drinks are running low on stock:\n'
            for drink in drinks:
                message += f'- {drink.name}\n'
            send_mail(
                'Low Stock Notification',
                message,
                'admin@yourdomain.com',
                ['manager@yourdomain.com'],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('Low stock'))
