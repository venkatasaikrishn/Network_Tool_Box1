import requests
from bs4 import BeautifulSoup
from dateutil import parser
from django.core.management.base import BaseCommand
from articles.models import Article
from datetime import datetime
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

class Command(BaseCommand):
    help = 'Fetch articles from multiple sources: BleepingComputer, Morning Brew, IT Brew'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            choices=['bleepingcomputer', 'morningbrew', 'itbrew', 'all'],
            default='all',
            help='Specify which source to fetch from'
        )

    def handle(self, *args, **options):
        source = options['source']
        
        if source == 'all' or source == 'bleepingcomputer':
            self.fetch_bleepingcomputer()
        
        if source == 'all' or source == 'morningbrew':
            self.fetch_morningbrew()
        
        if source == 'all' or source == 'itbrew':
            self.fetch_itbrew()

    def extract_author(self, soup, source_name):
        """Extract author with multiple fallback strategies"""
        author = None
        
        # Source-specific selectors
        if source_name == 'bleepingcomputer':
            selectors = [
                '.author > a',
                '.author',
                '.byline a',
                '.byline',
                '[rel="author"]',
                '.post-author',
                '.article-author',
                '.author-name',
                'span.author',
                'div.author'
            ]
        else:  # morningbrew and itbrew
            selectors = [
                '.author-name',
                '.byline a',
                '.byline',
                '[rel="author"]',
                '.author',
                '.post-author'
            ]
        
        # Try each selector
        for selector in selectors:
            author_tag = soup.select_one(selector)
            if author_tag:
                author_text = author_tag.get_text(strip=True)
                if author_text and author_text.lower() not in ['unknown', 'n/a', '', 'by', 'author']:
                    author = author_text
                    break
        
        # Fallback: look for meta tags
        if not author:
            meta_author = soup.find('meta', {'name': 'author'})
            if meta_author:
                author = meta_author.get('content', '').strip()
        
        # Fallback: look for schema.org markup
        if not author:
            script_tags = soup.find_all('script', type='application/ld+json')
            for script in script_tags:
                try:
                    import json
                    data = json.loads(script.string)
                    if isinstance(data, dict):
                        if 'author' in data:
                            if isinstance(data['author'], dict):
                                author = data['author'].get('name', '')
                            else:
                                author = data['author']
                        elif 'creator' in data:
                            author = data['creator']
                        if author:
                            break
                except:
                    continue
        
        return author if author else None

    def extract_published_date(self, soup, source_name):
        """Extract published date with multiple fallback strategies"""
        published_date = None
        
        # Source-specific selectors
        if source_name == 'bleepingcomputer':
            selectors = [
                'time[datetime]',
                'time',
                '.published-date',
                '.post-date',
                '.date',
                '[property="article:published_time"]',
                '.article-date',
                '.entry-date'
            ]
        else:  # morningbrew and itbrew
            selectors = [
                'time[datetime]',
                'time',
                '.published-date',
                '.post-date',
                '.date',
                '[property="article:published_time"]'
            ]
        
        # Try each selector
        for selector in selectors:
            date_tag = soup.select_one(selector)
            if date_tag:
                try:
                    # Try datetime attribute first
                    date_str = date_tag.get('datetime')
                    if not date_str:
                        date_str = date_tag.get_text(strip=True)
                    
                    if date_str:
                        # Clean up the date string
                        date_str = re.sub(r'\s+', ' ', date_str.strip())
                        published_date = parser.parse(date_str, fuzzy=True)
                        break
                except (ValueError, TypeError):
                    continue
        
        # Fallback: look for meta tags
        if not published_date:
            meta_date = soup.find('meta', {'property': 'article:published_time'})
            if not meta_date:
                meta_date = soup.find('meta', {'name': 'published_date'})
            if not meta_date:
                meta_date = soup.find('meta', {'name': 'date'})
            
            if meta_date:
                try:
                    date_str = meta_date.get('content', '').strip()
                    if date_str:
                        published_date = parser.parse(date_str, fuzzy=True)
                except (ValueError, TypeError):
                    pass
        
        # Fallback: look for schema.org markup
        if not published_date:
            script_tags = soup.find_all('script', type='application/ld+json')
            for script in script_tags:
                try:
                    import json
                    data = json.loads(script.string)
                    if isinstance(data, dict):
                        date_str = data.get('datePublished') or data.get('publishedDate')
                        if date_str:
                            published_date = parser.parse(date_str, fuzzy=True)
                            break
                except:
                    continue
        
        return published_date

    def fetch_bleepingcomputer(self):
        """Fetch articles from BleepingComputer"""
        self.stdout.write("🔍 Fetching from BleepingComputer...")
        url = 'https://www.bleepingcomputer.com/'
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to fetch BleepingComputer. Error: {e}"))
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('.bc_latest_news .bc_latest_news_text h4 a')[:5]
        count = 0

        for article_link in articles:
            try:
                title = article_link.get_text(strip=True)
                link = article_link['href']
                full_link = link if link.startswith("http") else "https://www.bleepingcomputer.com" + link

                # Fetch individual article page
                article_resp = requests.get(full_link, headers=HEADERS, timeout=10)
                if article_resp.status_code != 200:
                    continue

                article_soup = BeautifulSoup(article_resp.text, 'html.parser')

                # Extract author and published date
                author = self.extract_author(article_soup, 'bleepingcomputer')
                published_date = self.extract_published_date(article_soup, 'bleepingcomputer')

                # Save if not already exists
                if not Article.objects.filter(title=title).exists():
                    Article.objects.create(
                        title=title,
                        link=full_link,
                        author=author,
                        published_date=published_date,
                        source='BleepingComputer'
                    )
                    count += 1
                    self.stdout.write(f"✅ Saved: {title[:50]}...")

            except Exception as e:
                self.stdout.write(f"⚠️ Error processing article: {e}")
                continue

        self.stdout.write(self.style.SUCCESS(f"✅ Fetched {count} new articles from BleepingComputer."))

    def fetch_morningbrew(self):
        """Fetch articles from Morning Brew"""
        self.stdout.write("🔍 Fetching from Morning Brew...")
        url = 'https://www.morningbrew.com/daily'
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to fetch Morning Brew. Error: {e}"))
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try multiple selectors for Morning Brew
        article_selectors = [
            'a[href*="/stories/"]',
            'article a[href*="/stories/"]',
            'h2 a',
            'h3 a',
            'article h2 a',
            'article h3 a',
            'article .entry-title a',
            'article .post-title a',
            'article .title a'
        ]
        
        articles = []
        for selector in article_selectors:
            found_articles = soup.select(selector)
            if found_articles:
                articles = found_articles[:5]
                break
        
        count = 0

        for article_link in articles:
            try:
                title = article_link.get_text(strip=True)
                link = article_link['href']
                full_link = link if link.startswith("http") else "https://www.morningbrew.com" + link

                # Fetch individual article page
                article_resp = requests.get(full_link, headers=HEADERS, timeout=10)
                if article_resp.status_code != 200:
                    continue

                article_soup = BeautifulSoup(article_resp.text, 'html.parser')

                # Extract author and published date
                author = self.extract_author(article_soup, 'morningbrew')
                published_date = self.extract_published_date(article_soup, 'morningbrew')

                # Save if not already exists
                if not Article.objects.filter(title=title).exists():
                    Article.objects.create(
                        title=title,
                        link=full_link,
                        author=author,
                        published_date=published_date,
                        source='Morning Brew'
                    )
                    count += 1
                    self.stdout.write(f"✅ Saved: {title[:50]}...")

            except Exception as e:
                self.stdout.write(f"⚠️ Error processing article: {e}")
                continue

        self.stdout.write(self.style.SUCCESS(f"✅ Fetched {count} new articles from Morning Brew."))

    def fetch_itbrew(self):
        """Fetch articles from IT Brew"""
        self.stdout.write("🔍 Fetching from IT Brew...")
        url = 'https://www.itbrew.com/'
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to fetch IT Brew. Error: {e}"))
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try multiple selectors to find article links
        article_selectors = [
            'article h2 a',
            'article h3 a', 
            'article .entry-title a',
            'article .post-title a',
            'article .title a',
            'article a[href*="/202"]',  # Articles with year in URL
            'article a[href*="/article"]',
            'article a[href*="/post"]'
        ]
        
        articles = []
        for selector in article_selectors:
            found_articles = soup.select(selector)
            if found_articles:
                articles.extend(found_articles[:5])  # Limit per selector
                break
        
        # If no articles found with specific selectors, try broader approach
        if not articles:
            all_links = soup.select('article a[href*="/"]')
            articles = [link for link in all_links if self.is_valid_article_link(link)]
        
        count = 0

        for article_link in articles[:5]:  # Limit to 5 articles
            try:
                title = article_link.get_text(strip=True)
                link = article_link['href']
                
                # Skip if title is too short or contains common non-article text
                if not self.is_valid_article_title(title):
                    continue
                
                full_link = link if link.startswith("http") else "https://www.itbrew.com" + link

                # Fetch individual article page
                article_resp = requests.get(full_link, headers=HEADERS, timeout=10)
                if article_resp.status_code != 200:
                    continue

                article_soup = BeautifulSoup(article_resp.text, 'html.parser')

                # Extract author and published date
                author = self.extract_author(article_soup, 'itbrew')
                published_date = self.extract_published_date(article_soup, 'itbrew')

                # Save if not already exists
                if not Article.objects.filter(title=title).exists():
                    Article.objects.create(
                        title=title,
                        link=full_link,
                        author=author,
                        published_date=published_date,
                        source='IT Brew'
                    )
                    count += 1
                    self.stdout.write(f"✅ Saved: {title[:50]}...")

            except Exception as e:
                self.stdout.write(f"⚠️ Error processing article: {e}")
                continue

        self.stdout.write(self.style.SUCCESS(f"✅ Fetched {count} new articles from IT Brew."))

    def is_valid_article_title(self, title):
        """Check if the title is a valid article title"""
        if not title or len(title.strip()) < 10:
            return False
        
        # Skip common non-article text
        skip_words = ['read more', 'register', 'subscribe', 'login', 'sign up', 'contact', 'about', 'privacy', 'terms']
        title_lower = title.lower()
        
        for word in skip_words:
            if word in title_lower:
                return False
        
        return True

    def is_valid_article_link(self, link):
        """Check if the link is likely an article link"""
        href = link.get('href', '')
        title = link.get_text(strip=True)
        
        # Skip if no href or title
        if not href or not title:
            return False
        
        # Skip navigation and utility links
        skip_patterns = ['#', 'javascript:', 'mailto:', 'tel:']
        for pattern in skip_patterns:
            if pattern in href.lower():
                return False
        
        # Check if it's a valid article title
        return self.is_valid_article_title(title)