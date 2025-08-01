from django.core.management.base import BaseCommand
from articles.models import Article
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Clear all articles and fetch fresh top 5 from each source'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all articles'
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(self.style.WARNING("⚠️ This will delete ALL existing articles!"))
            self.stdout.write("Run with --confirm to proceed")
            return
        
        # Clear all articles
        count = Article.objects.count()
        Article.objects.all().delete()
        self.stdout.write(f"🗑️ Deleted {count} existing articles")
        
        # Fetch fresh articles from all sources
        self.stdout.write("🔄 Fetching fresh articles from all sources...")
        call_command('fetcharticles', '--source', 'all')
        
        # Show final count
        final_count = Article.objects.count()
        self.stdout.write(self.style.SUCCESS(f"✅ Total articles now: {final_count}"))
        
        # Show breakdown by source
        for source in ['BleepingComputer', 'Morning Brew', 'IT Brew']:
            count = Article.objects.filter(source=source).count()
            self.stdout.write(f"📰 {source}: {count} articles") 