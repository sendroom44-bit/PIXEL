import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create PIXEL administrator from environment variables"

    def handle(self, *args, **options):
        if os.environ.get("DJANGO_CREATE_SUPERUSER") != "1":
            self.stdout.write("Creation disabled.")
            return

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not email or not password:
            raise ValueError("Missing admin environment variables.")

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            self.stdout.write("This username already exists.")
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(self.style.SUCCESS("PIXEL admin created."))
