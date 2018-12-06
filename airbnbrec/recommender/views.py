from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Listing, Offering

def home(request):
	return render(request, 'recommender/homePage.html')

def customize(request):
	if request.method == 'POST':
		#read information from the POST
		request.session['neighborhood']=request.POST['where']
		request.session['checkin']=request.POST['checkin']
		request.session['checkout']=request.POST['checkout']
		minPriceNight=request.POST['minPrice']
		maxPriceNight=request.POST['maxPrice']
		request.session['numGuests']=request.POST['guests']
		request.session['numBeds']=request.POST['beds']
		request.session['numRooms']=request.POST['rooms']
		#find the number of nights from checkin and checkout
		checkinDate=datetime.strptime(checkin, '%Y-%m-%d')
		checkoutDate=datetime.strptime(checkout, '%Y-%m-%d')
		daysbetween=checkoutDate-checkinDate
		request.session['nights']=daysbetween.days+1 #inclusive
		#find total min and max price for entire stay
		request.session['minPrice']=int(minPriceNight)*nights
		request.session['maxPrice']=int(maxPriceNight)*nights

		return render(request, 'recommender/customizePage.html', context)
	return render(request, 'recommender/homePage.html') #need to change this to retry submit if POST didn't send

def load(request):
	return render(request, 'recommender/spinnyBoi.html')

def listing(request):
	neighborhood = request.session.get('neighborhood')
	checkin = request.session.get('checkin')
	checkout = request.session.get('checkout')
	numGuests = request.session.get('numGuests')
	numBeds = request.session.get('numBeds')
	numRooms = request.session.get('numRooms')
	nights = request.session.get('nights')
	minPrice = request.session.get('minPrice')
	maxPrice = request.session.get('maxPrice')
	#run the SQL query using these parameters and give the results to match page
	matches=Listing.objects.raw("SELECT DISTINCT id, listing_url FROM Listing AS l, Offering WHERE %s=neighborhood AND accommodates>=%s AND guests_included<=%s AND %s=(SELECT COUNT(*) FROM Offering WHERE date_for_stay<=%s AND date_for_stay>=%s AND available='t' AND listing_id=l.id) AND %s::MONEY<=(((%s-guests_included)*extra_people*%s)::MONEY + (SELECT SUM(price) FROM Offering WHERE date_for_stay<=%s AND date_for_stay>=%s AND listing_id=l.id)) AND %s::MONEY>=(((%s-guests_included)*extra_people*%s)::MONEY + (SELECT SUM(price) FROM Offering WHERE date_for_stay<=%s AND date_for_stay>=%s AND listing_id=l.id)) AND %s>=minimum_nights AND %s<=maximum_nights AND %s<=bedrooms AND %s<=beds", [neighborhood, numGuests, numGuests, nights, checkout, checkin, minPrice, numGuests, nights, checkout, checkin, maxPrice, numGuests, nights, checkout, checkin, nights, nights, numRooms, numBeds])
	context = {'matches': matches}

	if request.method == 'POST':
		diversity = request.POST['diversity']
		cuisine = request.POST['cuisine']
		name = request.POST['name']
		price = request.POST['price']
		diet = request.POST['diet']
		
	return render(request, 'recommender/listingDisplayPage.html')

def simple(request):
	top_listings=Listing.objects.order_by('-id')[:5] #we can change this to order by match_weight later	
	context = {'top_listings': top_listings}
	return render(request, 'recommender/simple.html', context) 

def match(request):
	if request.method == 'POST':
		#read information from the POST
		neighborhood=request.POST['where']
		checkin=request.POST['checkin']
		checkout=request.POST['checkout']
		minPriceNight=request.POST['minPrice']
		maxPriceNight=request.POST['maxPrice']
		numGuests=request.POST['guests']
		numBeds=request.POST['beds']
		numRooms=request.POST['rooms']
		#find the number of nights from checkin and checkout
		checkinDate=datetime.strptime(checkin, '%Y-%m-%d')
		checkoutDate=datetime.strptime(checkout, '%Y-%m-%d')
		daysbetween=checkoutDate-checkinDate
		nights=daysbetween.days+1 #inclusive
		#find total min and max price for entire stay
		minPrice=int(minPriceNight)*nights
		maxPrice=int(maxPriceNight)*nights
		#run the SQL query using these parameters and give the results to match page
		matches=Listing.objects.raw("SELECT DISTINCT id, listing_url FROM Listing AS l, Offering WHERE %s=neighborhood AND accommodates>=%s AND guests_included<=%s AND %s=(SELECT COUNT(*) FROM Offering WHERE date_for_stay<=%s AND date_for_stay>=%s AND available='t' AND listing_id=l.id) AND %s::MONEY<=(((%s-guests_included)*extra_people*%s)::MONEY + (SELECT SUM(price) FROM Offering WHERE date_for_stay<=%s AND date_for_stay>=%s AND listing_id=l.id)) AND %s::MONEY>=(((%s-guests_included)*extra_people*%s)::MONEY + (SELECT SUM(price) FROM Offering WHERE date_for_stay<=%s AND date_for_stay>=%s AND listing_id=l.id)) AND %s>=minimum_nights AND %s<=maximum_nights AND %s<=bedrooms AND %s<=beds", [neighborhood, numGuests, numGuests, nights, checkout, checkin, minPrice, numGuests, nights, checkout, checkin, maxPrice, numGuests, nights, checkout, checkin, nights, nights, numRooms, numBeds])
		context = {'matches': matches}
		return render(request, 'recommender/simpleMatches.html', context)
	return render(request, 'recommender/simple.html')

# def customize(request):
# 	return render(request, 'recommender/customizePage.html')
