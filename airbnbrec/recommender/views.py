from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Listing, Offering

def home(request):
    return render(request, 'recommender/homePage.html')

def simple(request):
	top_listings=Listing.objects.order_by('-id')[:5] #we can change this to order by match_weight later
	context = {'top_listings': top_listings}
	return render(request, 'recommender/simple.html', context) 
