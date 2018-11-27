from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Listing, Offering

def home(request):
	return render(request, 'recommender/homePage.html')

def customize(request):
	return render(request, 'recommender/customizePage.html')

def load(request):
	return render(request, 'recommender/spinnyBoi.html')

def listing(request):
	return render(request, 'recommender/listingDisplayPage.html')

def simple(request):
	top_listings=Listing.objects.order_by('-id')[:5] #we can change this to order by match_weight later	
	context = {'top_listings': top_listings}
	return render(request, 'recommender/simple.html', context) 

def match(request):
	if request.method == 'POST':
		neighborhood=request.POST['where']
		checkin=request.POST['checkin']
		checkout=request.POST['checkout']
		minPrice=request.POST['minPrice']
		maxPrice=request.POST['maxPrice']
		numGuests=request.POST['guests']
		numBeds=request.POST['beds']
		numRooms=request.POST['rooms']
		nights=3;
		# return HttpResponseRedirect('top5/')
		# matches=Listing.objects.raw('SELECT DISTINCT id, listing_url FROM Listing AS l, Offering WHERE %s=neighborhood AND accommodates>=%s AND guests_included<=%s AND %s=(SELECT COUNT(*) FROM Offering WHERE date_for_stay<=to_date(%s, 'MM/DD/YYYY') AND date_for_stay>=to_date(%s, 'MM/DD/YYYY') AND available='t' AND listing_id=l.id) AND %s::MONEY<=(((%s-guests_included)*extra_people*%s)::MONEY + (SELECT SUM(price) FROM Offering WHERE date_for_stay<=to_date(%s, 'MM/DD/YYYY') AND date_for_stay>=to_date(%s, 'MM/DD/YYYY') AND listing_id=l.id)) AND %s::MONEY>=(((%s-guests_included)*extra_people*%s)::MONEY + (SELECT SUM(price) FROM Offering WHERE date_for_stay<=to_date(%s, 'MM/DD/YYYY') AND date_for_stay>=to_date(%s, 'MM/DD/YYYY') AND listing_id=l.id)) AND %s>=minimum_nights AND %s<=maximum_nights AND %s<=bedrooms AND %s<=beds;', [neighborhood, numGuests, numGuests, nights, checkout, checkin, minPrice, numGuests, nights, checkout, checkin, maxPrice, numGuests, nights, checkout, checkin, nights, nights, numRooms, numBeds])
		# context = {'matches': matches}
		# return render(request, 'recommender/topmatch.html', context)
		return render(request, 'recommender/simpleMatches.html')

def customize(request):
	return render(request, 'recommender/customizePage.html')
