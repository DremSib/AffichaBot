from django.shortcuts import render
from .models import request_database

def index(request):
    database = request_database()
    return render(request, 'main/index.html', {'content': database, 'user_id': })