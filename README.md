# 📰 Tech News Digest

> **Your daily dose of curated tech news from the world's leading publications**

A modern, automated news aggregation platform that fetches and displays the latest tech articles from multiple sources in a beautiful, responsive interface.

![Tech News Digest](https://img.shields.io/badge/Django-4.2+-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Automation](https://img.shields.io/badge/Automation-Enabled-success)

## ✨ Features

### 🎯 **Core Features**
- **Multi-Source Aggregation**: Fetches articles from BleepingComputer, Morning Brew, and IT Brew
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Real-time Counts**: Accurate article counts for each source
- **Automatic Updates**: Scheduled fetching every 30 minutes
- **Duplicate Prevention**: Smart detection to avoid duplicate articles
- **Error Handling**: Robust error handling and logging

### 🤖 **Automation**
- **Zero Maintenance**: Fully automated article fetching
- **Background Processing**: Runs silently in the background
- **Logging**: Complete activity logging for monitoring
- **Windows Task Scheduler**: Easy setup for Windows users

### 📊 **Smart Analytics**
- **Source Tracking**: Individual counts for each news source
- **Update Timestamps**: Shows when articles were last updated
- **Article Metadata**: Author, publication date, and source information

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Windows 10/11 (for Task Scheduler automation)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd finalprojectt
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django requests beautifulsoup4 python-dateutil
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Visit the application**
   ```
   http://localhost:8000
   ```

## 📰 Fetching Articles

### Manual Fetch
```bash
# Fetch from all sources
python manage.py fetcharticles

# Fetch from specific source
python manage.py fetcharticles --source bleepingcomputer
python manage.py fetcharticles --source morningbrew
python manage.py fetcharticles --source itbrew
```

### Automated Fetch
```bash
# Test automation
python manage.py auto_fetch_articles

# Run the batch file (Windows)
.\run_auto_fetch.bat
```

## 🤖 Setting Up Automation

### Windows Task Scheduler Setup

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`, press Enter

2. **Create Basic Task**
   - Name: `Tech News Auto Fetch`
   - Trigger: Daily
   - Action: Start a program

3. **Configure Program**
   ```
   Program: C:\Users\user\finalprojectt\run_auto_fetch.bat
   Start in: C:\Users\user\finalprojectt
   ```

4. **Set Advanced Settings**
   - Triggers → Edit → Advanced Settings
   - Check "Repeat task every:" → 30 minutes
   - Duration: Indefinitely

## 📁 Project Structure

```
finalprojectt/
├── articles/
│   ├── management/commands/
│   │   ├── auto_fetch_articles.py    # Automation command
│   │   └── fetcharticles.py          # Main fetching logic
│   ├── templates/articles/
│   │   └── article_list.html         # Beautiful UI template
│   ├── models.py                     # Article data model
│   ├── views.py                      # View logic with smart counts
│   └── urls.py                       # URL routing
├── technews/
│   ├── settings.py                   # Django settings
│   └── urls.py                       # Main URL configuration
├── run_auto_fetch.bat                # Windows automation script
├── manage.py                         # Django management
└── db.sqlite3                        # Article database
```

## 🎨 UI Features

### **Modern Design**
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Smooth Animations**: Fade-in and slide-up effects
- **Gradient Backgrounds**: Beautiful purple-blue gradients
- **Card-based Layout**: Clean article cards with hover effects

### **Interactive Elements**
- **Source Filtering**: Visual source badges
- **External Links**: Direct links to original articles
- **Scroll-to-Top**: Floating action button
- **Hover Effects**: Interactive card animations

### **Information Display**
- **Article Counts**: Real-time counts for each source
- **Update Timestamps**: Shows when content was last updated
- **Author Information**: Displays article authors when available
- **Publication Dates**: Shows when articles were published

## 🔧 Configuration

### **Adding New Sources**
Edit `articles/management/commands/fetcharticles.py`:
```python
def fetch_new_source(self):
    """Add your new source here"""
    # Implementation for new source
```

### **Changing Fetch Frequency**
- **Task Scheduler**: Edit the repeat interval
- **Cron (Linux/Mac)**: Modify cron schedule
- **Docker**: Update cron configuration

### **Modifying Article Count**
Edit the fetch methods in `fetcharticles.py`:
```python
articles = soup.select('selector')[:10]  # Change 5 to 10 for more articles
```

## 📊 Data Sources

| Source | Description | Article Count |
|--------|-------------|---------------|
| **BleepingComputer** | Cybersecurity and tech news | Top 5 articles |
| **Morning Brew** | Daily tech newsletter | Top 5 articles |
| **IT Brew** | IT industry insights | Top 5 articles |

## 🛠️ Technical Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, Tailwind CSS
- **Icons**: Font Awesome 6.0
- **Animations**: CSS3 animations and JavaScript
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **Automation**: Windows Task Scheduler + Batch scripts

## 📝 Logging

All automation activities are logged to:
- **Console Output**: Real-time feedback during fetching
- **Task Scheduler Logs**: Windows event logs
- **Application Logs**: Django logging system

## 🚀 Deployment

### **Local Development**
```bash
python manage.py runserver
```

### **Production Considerations**
- Use PostgreSQL for better performance
- Set up proper logging
- Configure static files
- Use environment variables for settings
- Set up proper backup for the database

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Django**: The web framework for perfectionists
- **Tailwind CSS**: A utility-first CSS framework
- **Font Awesome**: The iconic font and CSS toolkit
- **Beautiful Soup**: Python library for web scraping

---

**Made with ❤️ using Django**

*Your daily tech news, automatically curated and beautifully presented.* 