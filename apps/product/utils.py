from django.conf import settings
from django.core.mail import send_mail


def send_stock_alert_email(self, stock_status):
    send_mail(
        subject=f'Alert: {self.name} is {stock_status}',
        message=f'The product "{self.name}" is currently {stock_status}. '
                f'Please review the stock level and consider restocking.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['inventory_manager@example.com'],
        fail_silently=False,
    )