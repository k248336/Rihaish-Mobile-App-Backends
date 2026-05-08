from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import sys


class Command(BaseCommand):
    help = 'Test email sending configuration'

    def add_arguments(self, parser):
        parser.add_argument('recipient_email', type=str, help='Email address to send test email to')

    def handle(self, *args, **options):
        recipient = options['recipient_email']
        
        self.stdout.write(self.style.SUCCESS(f'Testing email configuration...'))
        self.stdout.write(f'EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
        
        if not settings.EMAIL_HOST_USER:
            self.stdout.write(self.style.ERROR('ERROR: EMAIL_HOST_USER is not set!'))
            sys.exit(1)
            
        if not settings.EMAIL_HOST_PASSWORD:
            self.stdout.write(self.style.ERROR('ERROR: EMAIL_HOST_PASSWORD is not set!'))
            sys.exit(1)

        try:
            self.stdout.write(f'\nSending test email to {recipient}...')
            send_mail(
                subject='Test Email from Rihaish',
                message='This is a test email to verify your email configuration is working!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('✓ Email sent successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Failed to send email: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
            sys.exit(1)
