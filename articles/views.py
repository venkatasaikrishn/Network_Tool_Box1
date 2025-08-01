from django.shortcuts import render
from .models import Article

def article_list(request):
    articles = Article.objects.order_by('-id')  # Or '-published_date' if it's sortable
    return render(request, 'articles/article_list.html', {'articles': articles})
