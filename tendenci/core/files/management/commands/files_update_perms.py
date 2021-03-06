from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    example: python manage.py files_update_perms.py
    """
    def handle(self, *args, **kwargs):
        from django.db import connection, transaction
        cursor = connection.cursor()

        cursor.execute("UPDATE files_file SET allow_anonymous_view = 1 WHERE is_public = 1")
        transaction.commit_unless_managed()