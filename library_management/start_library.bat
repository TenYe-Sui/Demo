@echo off
echo Starting Django Development Server...
start cmd /k "python manage.py runserver"

echo Starting Celery Worker...
start cmd /k "celery -A library_management worker --loglevel=info"

echo Starting Celery Beat...
start cmd /k "celery -A library_management beat --loglevel=info"

echo All processes have been started.
pause