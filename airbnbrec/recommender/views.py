from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Listing, Offering, Business
from datetime import datetime
from operator import itemgetter

def home(request):
	return render(request, 'recommender/homePage.html')

def customize(request):
	#store user input for the airbnb listing
	if request.method == 'POST':
		#read information from the POST
		request.session['neighborhood']=request.POST['where']
		checkin = request.POST['checkin']
		checkout = request.POST['checkout']
		request.session['checkin']=checkin
		request.session['checkout']=checkout
		minPriceNight=request.POST['minPrice']
		maxPriceNight=request.POST['maxPrice']
		request.session['numGuests']=request.POST['guests']
		request.session['numBeds']=request.POST['beds']
		request.session['numRooms']=request.POST['rooms']
		#find the number of nights from checkin and checkout
		checkinDate=datetime.strptime(checkin, '%Y-%m-%d')
		checkoutDate=datetime.strptime(checkout, '%Y-%m-%d')
		daysbetween=checkoutDate-checkinDate
		nights = daysbetween.days+1 #inclusive
		request.session['nights']=nights
		#find total min and max price for entire stay
		request.session['minPrice']=int(minPriceNight)*nights
		request.session['maxPrice']=int(maxPriceNight)*nights

		return render(request, 'recommender/customizePage.html')
	return render(request, 'recommender/homePage.html') #need to change this to retry submit if POST didn't send

def load(request):
	#store user input for food
	if request.method == 'POST':
		request.session['diversity'] = request.POST['diversity']
		request.session['cuisine'] = request.POST['cuisine']
		request.session['restaurant'] = request.POST['type']
		request.session['foodPrice'] = request.POST['price']
		request.session['diet'] = request.POST['diet']
		request.session['p1'] = request.POST['priority1']
		request.session['p2'] = request.POST['priority2']
		request.session['p3'] = request.POST['priority3']
		request.session['p4'] = request.POST['priority4']
		request.session['p5'] = request.POST['priority5']

	return render(request, 'recommender/listingDisplayPage.html')

def listing(request):
	#retrieve user input for airbnb listing
	neighborhood = request.session.get('neighborhood')
	checkin = request.session.get('checkin')
	checkout = request.session.get('checkout')
	numGuests = request.session.get('numGuests')
	numBeds = request.session.get('numBeds')
	numRooms = request.session.get('numRooms')
	nights = request.session.get('nights')
	minPrice = request.session.get('minPrice')
	maxPrice = request.session.get('maxPrice')
	
	#retrieve user input for food
	# diversity = request.session.get('diversity')
	# cuisine = request.session.get('cuisine')
	# restaurant = request.session.get('restaurant')
	# foodPrice = request.session.get('foodPrice')
	# diet = request.session.get('diet')

	# #retrieve user ranking of the Yelp options above
	# #can be the strings "cuisine", "diversity", "diet", "price", and "type"
	# p1 = request.session.get('p1')
	# p2 = request.session.get('p2')
	# p3 = request.session.get('p3')
	# p4 = request.session.get('p4')
	# p5 = request.session.get('p5')

	if request.method == 'POST':
		diversity= request.POST['diversity']
		cuisine= request.POST['cuisine']
		restaurant= request.POST['type']
		foodPrice= request.POST['price']
		diet= request.POST['diet']
		p1= request.POST['priority1']
		p2= request.POST['priority2']
		p3= request.POST['priority3']
		p4= request.POST['priority4']
		p5= request.POST['priority5']

	#run the SQL query using these parameters and give the results to match page
	matches=Listing.objects.raw("SELECT DISTINCT id, listing_url, name, description, neighborhood, accommodates FROM Listing AS l, Offering WHERE %s=neighborhood AND accommodates>=%s AND guests_included<=%s AND %s=(SELECT COUNT(*) FROM Offering WHERE date_for_stay<=%s AND date_for_stay>=%s AND available='t' AND listing_id=l.id) AND %s::MONEY<=(((%s-guests_included)*extra_people*%s)::MONEY + (SELECT SUM(price) FROM Offering WHERE date_for_stay<=%s AND date_for_stay>=%s AND listing_id=l.id)) AND %s::MONEY>=(((%s-guests_included)*extra_people*%s)::MONEY + (SELECT SUM(price) FROM Offering WHERE date_for_stay<=%s AND date_for_stay>=%s AND listing_id=l.id)) AND %s>=minimum_nights AND %s<=maximum_nights AND %s<=bedrooms AND %s<=beds", [neighborhood, numGuests, numGuests, nights, checkout, checkin, minPrice, numGuests, nights, checkout, checkin, maxPrice, numGuests, nights, checkout, checkin, nights, nights, numRooms, numBeds])
	matches=list(matches)	
	if len(matches)==0:
		return render(request, 'recommender/noListingPage.html')


	# maxscore=0
	# toplisting=''
	listings=[]
	for i in range(len(matches)):
		allbusinesses= Business.objects.raw("SELECT * FROM Business WHERE 2 * 3961 * asin( sqrt((sin( radians(  (%s - Business.latitude) / 2 ))) ^ 2  + cos(radians(%s)) * cos(radians(Business.latitude)) * (sin( radians((%s - Business.longitude) / 2) ) ) ^ 2) )   < 5", [matches[i].latitude, matches[i].latitude, matches[i].longitude])
		# allbusinesses= Business.objects.raw("SELECT * FROM Business sqrt((1545049/324 * SQUARE(%s- Business.latitude))+(620059801/129600*SQUARE( (%s - Business.longitude) * cos( (%s+ Business.latitude)/2 ))) ) < 1", [matches[i].latitude, matches[i].longitude, matches[i].latitude])
		allbusinesses=list(allbusinesses)
		businesscount= len(allbusinesses)
		
		divset = set()
		cuisinecount=0;
		restaurantcount=0;
		pricecount=0;
		dietcount=0;
		for business in allbusinesses:
			divset.add(business.category)
			if business.category==cuisine:
				cuisinecount+=1
			if business.category==restaurant:
				restaurantcount+=1
			if business.price==foodPrice:
				pricecount+=1
			if business.category==diet:
				dietcount+=1
		diversitycount = len(divset)
		
		wc=0
		wr=0
		wd=0
		wdv=0
		wp=0

		if p1=='cuisine':
		 	wc=.3
		if p2=='cuisine':
		 	wc=.25	
		if p3=='cuisine':
		 	wc=.2
		if p4=='cuisine':
		 	wc=.15
		if p5=='cuisine':
		 	wc=.1

		if p1=='restaurant':
		 	wr=.3
		if p2=='restaurant':
		 	wr=.25	
		if p3=='restaurant':
		 	wr=.2
		if p4=='restaurant':
		 	wr=.15
		if p5=='restaurant':
		 	wr=.1

		if p1=='diet':
		 	wd=.3
		if p2=='diet':
		 	wd=.25	
		if p3=='diet':
		 	wd=.2
		if p4=='diet':
		 	wd=.15
		if p5=='diet':
		 	wd=.1

		if p1=='diversity':
		 	wdv=.3
		if p2=='diversity':
		 	wdv=.25	
		if p3=='diversity':
		 	wdv=.2
		if p4=='diversity':
		 	wdv=.15
		if p5=='diversity':
		 	wdv=.1


		if p1=='price':
		 	wp=.3
		if p2=='price':
		 	wp=.25	
		if p3=='price':
		 	wp=.2
		if p4=='price':
		 	wp=.15
		if p5=='price':
		 	wp=.1

		score= wc* cuisinecount/businesscount + wr*restaurantcount/businesscount+ wdv*diversitycount/113+wd*dietcount/businesscount+ wp*pricecount/businesscount
		# if score>=maxscore:
		# 	maxscore=score
		# 	toplisting=matches[i].listing_url
		listings.append((matches[i], score))
	listings.sort(key=itemgetter(1), reverse=True)


	context={'listings':listings}
	# return render(request, 'recommender/simpleMatches.html', context)
	# context = {'diversity': diversity, 'cuisine': cuisine, 'restaurant':restaurant, 'foodPrice':foodPrice, 'diet':diet, 'listingurl':toplisting}
	return render(request, 'recommender/listingDisplayPage.html', context)

def nolisting(request):
	return render(request, 'recommender/noListingPage.html')
