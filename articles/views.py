from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from .models import Article

def article_list(request):
    articles = Article.objects.order_by('-id')
    
    # Get counts for each source in a single query
    source_counts = Article.objects.values('source').annotate(count=Count('id'))
    
    # Create a dictionary for easy lookup
    counts_dict = {item['source']: item['count'] for item in source_counts}
    
    context = {
        'articles': articles,
        'bleepingcomputer_count': counts_dict.get('BleepingComputer', 0),
        'morningbrew_count': counts_dict.get('Morning Brew', 0),
        'itbrew_count': counts_dict.get('IT Brew', 0),
        'now': timezone.now(),
    }
    
    return render(request, 'articles/article_list.html', context)
