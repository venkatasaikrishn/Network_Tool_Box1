@echo off
cd /d "C:\Users\user\finalprojectt"
call venv\Scripts\activate.bat
python manage.py auto_fetch_articles
pause 