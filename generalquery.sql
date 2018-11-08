SELECT DISTINCT id, listing_url
FROM Listing AS l, Offering
WHERE accommodates>=NUMPEOPLE
AND guests_included<=NUMPEOPLE
AND NIGHTS=(SELECT COUNT(*)
	FROM Offering
	WHERE date_for_stay<=to_date('LASTDATE', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('FIRSTDATE', 'MM/DD/YYYY')
	AND available='t'
	AND listing_id=l.id)
AND MINPRICE::MONEY<=(((NUMPEOPLE-guests_included)*extra_people*NIGHTS)::MONEY + (SELECT SUM(price)
	FROM Offering
	WHERE date_for_stay<=to_date('LASTDATE', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('FIRSTDATE', 'MM/DD/YYYY')
	AND listing_id=l.id))
AND MAXPRICE::MONEY>=(((NUMPEOPLE-guests_included)*extra_people*NIGHTS)::MONEY + (SELECT SUM(price)
	FROM Offering
	WHERE date_for_stay<=to_date('LASTDATE', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('FIRSTDATE', 'MM/DD/YYYY')
	AND listing_id=l.id))
AND NIGHTS>=minimum_nights
AND NIGHTS<=maximum_nights
AND BEDROOMS<=bedrooms
AND BEDS<=beds
AND 'NEIGHBORHOOD'=neighborhood;

required inputs: minPrice, maxPrice, firstDate, lastDate, nights, people, bedrooms, beds, neighborhood