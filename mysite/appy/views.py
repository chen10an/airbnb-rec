from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'appy/homePage.html')

def customize(request):
	return render(request, 'appy/customizePage.html')