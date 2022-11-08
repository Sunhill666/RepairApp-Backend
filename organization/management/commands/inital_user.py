from django.core.management.base import BaseCommand

from organization.models import User


class Command(BaseCommand):
    help = "初始化一个超级管理员"

    def handle(self, *args, **options):
        User.objects.create_superuser(username="10010", first_name="admin", last_name="root", password="ybh123")
