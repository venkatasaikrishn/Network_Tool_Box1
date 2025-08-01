import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from articles.management.commands.fetcharticles import Command as FetchCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Automatically fetch articles from all sources'

    def handle(self, *args, **options):
        try:
            self.stdout.write(f"🕐 Starting automatic article fetch at {timezone.now()}")
            
            # Use the existing fetch command
            fetch_command = FetchCommand()
            fetch_command.handle(source='all')
            
            self.stdout.write(self.style.SUCCESS(f"✅ Automatic fetch completed at {timezone.now()}"))
            logger.info(f"Automatic article fetch completed successfully at {timezone.now()}")
            
        except Exception as e:
            error_msg = f"❌ Automatic fetch failed: {e}"
            self.stdout.write(self.style.ERROR(error_msg))
            logger.error(f"Automatic article fetch failed: {e}")
            raise 