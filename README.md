# Tech News Digest

A Django web application that aggregates tech news from multiple sources and displays them in a beautiful, modern interface.

## Features

- **Multi-source aggregation**: Fetches articles from BleepingComputer, Morning Brew, and IT Brew
- **Beautiful UI**: Modern design with animations, gradients, and responsive layout
- **Source tracking**: Shows where each article was extracted from
- **Author and date extraction**: Automatically extracts author names and publication dates
- **Top 5 articles**: Gets the latest 5 articles from each source

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Fetch articles**:
   ```bash
   python manage.py fetcharticles
   ```

4. **Start the server**:
   ```bash
   python manage.py runserver
   ```

5. **Visit the website**: http://localhost:8000

## Commands

### Fetch Articles
```bash
# Fetch from all sources
python manage.py fetcharticles

# Fetch from specific source
python manage.py fetcharticles --source bleepingcomputer
python manage.py fetcharticles --source morningbrew
python manage.py fetcharticles --source itbrew
```

### Refresh All Articles
```bash
# Clear all articles and fetch fresh ones
python manage.py refresh_articles --confirm
```

## Manual Article Fetching

To fetch articles manually:

```bash
# Fetch from all sources
python manage.py fetcharticles

# Fetch from specific source
python manage.py fetcharticles --source bleepingcomputer
python manage.py fetcharticles --source morningbrew
python manage.py fetcharticles --source itbrew
```

## Automatic Fetching

For automatic article fetching, you can:

1. **Use Windows Task Scheduler** (create a scheduled task to run `python manage.py fetcharticles`)
2. **Use cron jobs** (Linux/Mac) to schedule the command
3. **Create a custom script** to run the command at intervals

The command will fetch the latest 5 articles from each source.

## Sources

- **BleepingComputer**: Cybersecurity and tech news
- **Morning Brew**: Business and tech news
- **IT Brew**: IT industry news

## Technologies Used

- **Django**: Web framework
- **BeautifulSoup**: Web scraping
- **Tailwind CSS**: Styling
- **Font Awesome**: Icons
- **Requests**: HTTP requests

## Project Structure

```
finalprojectt/
├── articles/
│   ├── models.py          # Article model
│   ├── views.py           # Article list view
│   ├── templates/         # HTML templates
│   └── management/        # Custom commands
├── technews/              # Django settings
└── manage.py             # Django management
``` 