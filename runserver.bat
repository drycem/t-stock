ECHO OFF
D: && cd D:\projects\django_api_react\.env\scripts && activate && cd D:\projects\django_api_react && start /b cmd /c python manage.py runserver && start "" http://127.0.0.1:8000
PAUSE