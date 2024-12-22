from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Drops the foreign key constraint from django_admin_log'

    def handle(self, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    ALTER TABLE django_admin_log
                    DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_profiles_profile_id
                """)
            self.stdout.write(self.style.SUCCESS("Constraint dropped successfully!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
