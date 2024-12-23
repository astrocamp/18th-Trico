from django.core.management.base import BaseCommand
from categories.models import Category

class Command(BaseCommand):
    help = "Seeds the database with categories"

    def handle(self, *args, **options):

        initial_categories = [
            {"name": "設計與創意", "created_at": "2024-12-23"},
            {"name": "技術程式開發", "created_at": "2024-12-23"},
            {"name": "寫作與內容創作", "created_at": "2024-12-23"},
            {"name": "行銷與廣告", "created_at": "2024-12-23"},
            {"name": "攝影創作", "created_at": "2024-12-23"},
            {"name": "顧問與專業服務", "created_at": "2024-12-23"},
            {"name": "生活娛樂", "created_at": "2024-12-23"},
        ]

        for category in initial_categories:

            result = Category.objects.get_or_create(
                name=category["name"], created_at=category["created_at"]
            )

            category = result[0]
            created = result[1]

            if created:
                self.stdout.write(self.style.SUCCESS(f"Category '{category.name}' created"))
            else:
                self.stdout.write(self.style.WARNING(f"Category '{category.name}' already exists"))