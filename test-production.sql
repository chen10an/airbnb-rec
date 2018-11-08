--General Format of queries:
--required inputs: MINPRICE, MAXPRICE, LASTDATE, FIRSTDATE, NIGHTS, NUMPEOPLE, BEDROOMS, BEDS, NEIGHBORHOOD

-- SELECT DISTINCT id, listing_url
-- FROM Listing AS l, Offering
-- WHERE accommodates>=NUMPEOPLE
-- AND guests_included<=NUMPEOPLE
-- AND NIGHTS=(SELECT COUNT(*)
-- 	FROM Offering
-- 	WHERE date_for_stay<=to_date('LASTDATE', 'MM/DD/YYYY')
-- 	AND date_for_stay>=to_date('FIRSTDATE', 'MM/DD/YYYY')
-- 	AND available='t'
-- 	AND listing_id=l.id)
-- AND MINPRICE::MONEY<=(((NUMPEOPLE-guests_included)*extra_people*NIGHTS)::MONEY + (SELECT SUM(price)
-- 	FROM Offering
-- 	WHERE date_for_stay<=to_date('LASTDATE', 'MM/DD/YYYY')
-- 	AND date_for_stay>=to_date('FIRSTDATE', 'MM/DD/YYYY')
-- 	AND listing_id=l.id))
-- AND MAXPRICE::MONEY>=(((NUMPEOPLE-guests_included)*extra_people*NIGHTS)::MONEY + (SELECT SUM(price)
-- 	FROM Offering
-- 	WHERE date_for_stay<=to_date('LASTDATE', 'MM/DD/YYYY')
-- 	AND date_for_stay>=to_date('FIRSTDATE', 'MM/DD/YYYY')
-- 	AND listing_id=l.id))
-- AND NIGHTS>=minimum_nights
-- AND NIGHTS<=maximum_nights
-- AND BEDROOMS<=bedrooms
-- AND BEDS<=beds
-- AND 'NEIGHBORHOOD'=neighborhood;

-------------------------------------------------------------------
/*Test1: Test Query
All listings returned should accomodate at least 3 people.
Guests_included should not exceed 3 people.
The total price of staying at the listing for 5 nights with 3 people
from 8/1/19-8/5/19 should be between $600 and $700.
Guests should be able to book the location for the 5 nights above.
There should be at least 1 bedroom and 2 beds.
The listing should be in Harlem.
*/

SELECT DISTINCT id, listing_url
FROM Listing AS l, Offering
WHERE accommodates>=3
AND guests_included<=3
AND 5=(SELECT COUNT(*)
	FROM Offering
	WHERE date_for_stay<=to_date('12/30/2018', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('12/26/2018', 'MM/DD/YYYY')
	AND available='t'
	AND listing_id=l.id)
AND 300::MONEY<=(((3-guests_included)*extra_people*5)::MONEY + (SELECT SUM(price)
	FROM Offering
	WHERE date_for_stay<=to_date('12/30/2018', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('12/26/2018', 'MM/DD/YYYY')
	AND listing_id=l.id))
AND 900::MONEY>=(((3-guests_included)*extra_people*5)::MONEY + (SELECT SUM(price)
	FROM Offering
	WHERE date_for_stay<=to_date('12/30/2018', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('12/26/2018', 'MM/DD/YYYY')
	AND listing_id=l.id))
AND 5>=minimum_nights
AND 5<=maximum_nights
AND 1<=bedrooms
AND 2<=beds
AND 'Harlem'=neighborhood;

/*
   id   |             listing_url
--------+-------------------------------------
 342995 | https://www.airbnb.com/rooms/342995
 855919 | https://www.airbnb.com/rooms/855919
 548815 | https://www.airbnb.com/rooms/548815
 385853 | https://www.airbnb.com/rooms/385853
(4 rows)
*/
-------------------------------------------------------------------
/*Test2: Test dates available
The only change in this query from Test1 are the dates being booked.
The additional listings in the results of this query are those
that were not available on 12/29/2018 and/or 12/30/2018.
Note: in other circumstances, changing the dates could also
cause some listings to leave the price range.
*/
SELECT DISTINCT id, listing_url
FROM Listing AS l, Offering
WHERE accommodates>=3
AND guests_included<=3
AND 5=(SELECT COUNT(*)
	FROM Offering
	WHERE date_for_stay<=to_date('12/28/2018', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('12/24/2018', 'MM/DD/YYYY')
	AND available='t'
	AND listing_id=l.id)
AND 300::MONEY<=(((3-guests_included)*extra_people*5)::MONEY + (SELECT SUM(price)
	FROM Offering
	WHERE date_for_stay<=to_date('12/28/2018', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('12/24/2018', 'MM/DD/YYYY')
	AND listing_id=l.id))
AND 900::MONEY>=(((3-guests_included)*extra_people*5)::MONEY + (SELECT SUM(price)
	FROM Offering
	WHERE date_for_stay<=to_date('12/28/2018', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('12/24/2018', 'MM/DD/YYYY')
	AND listing_id=l.id))
AND 5>=minimum_nights
AND 5<=maximum_nights
AND 1<=bedrooms
AND 2<=beds
AND 'Harlem'=neighborhood;

/*
   id   |             listing_url
--------+-------------------------------------
 342995 | https://www.airbnb.com/rooms/342995
 548815 | https://www.airbnb.com/rooms/548815
   8225 | https://www.airbnb.com/rooms/8225
 385853 | https://www.airbnb.com/rooms/385853
   2515 | https://www.airbnb.com/rooms/2515
 855919 | https://www.airbnb.com/rooms/855919
  58059 | https://www.airbnb.com/rooms/58059
(7 rows)
*/
-------------------------------------------------------------------
/*Test3: Test minimum_nights
For the purposes of this query, NIGHTS was changed only
when checking against minimum_nights and maximum_nights
so that results could be compared with those from Test1.
Listings returned should be those from Test1 that can be booked
for only 1 night. 
*/

SELECT DISTINCT id, listing_url
FROM Listing AS l, Offering
WHERE accommodates>=3
AND guests_included<=3
AND 5=(SELECT COUNT(*)
	FROM Offering
	WHERE date_for_stay<=to_date('12/30/2018', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('12/26/2018', 'MM/DD/YYYY')
	AND available='t'
	AND listing_id=l.id)
AND 300::MONEY<=(((3-guests_included)*extra_people*5)::MONEY + (SELECT SUM(price)
	FROM Offering
	WHERE date_for_stay<=to_date('12/30/2018', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('12/26/2018', 'MM/DD/YYYY')
	AND listing_id=l.id))
AND 900::MONEY>=(((3-guests_included)*extra_people*5)::MONEY + (SELECT SUM(price)
	FROM Offering
	WHERE date_for_stay<=to_date('12/30/2018', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('12/26/2018', 'MM/DD/YYYY')
	AND listing_id=l.id))
AND 1>=minimum_nights
AND 1<=maximum_nights
AND 1<=bedrooms
AND 2<=beds
AND 'Harlem'=neighborhood;

-------------------------------------------------------------------
/*Test4: Test maximum_nights
For the purposes of this query, NIGHTS was changed only
when checking against minimum_nights and maximum_nights
so that results could be compared with those from Test1.
Listings returned should be those from Test1 that can be booked
for 22 nights.
*/

SELECT DISTINCT id, listing_url
FROM Listing AS l, Offering
WHERE accommodates>=3
AND guests_included<=3
AND 5=(SELECT COUNT(*)
	FROM Offering
	WHERE date_for_stay<=to_date('12/30/2018', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('12/26/2018', 'MM/DD/YYYY')
	AND available='t'
	AND listing_id=l.id)
AND 300::MONEY<=(((3-guests_included)*extra_people*5)::MONEY + (SELECT SUM(price)
	FROM Offering
	WHERE date_for_stay<=to_date('12/30/2018', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('12/26/2018', 'MM/DD/YYYY')
	AND listing_id=l.id))
AND 900::MONEY>=(((3-guests_included)*extra_people*5)::MONEY + (SELECT SUM(price)
	FROM Offering
	WHERE date_for_stay<=to_date('12/30/2018', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('12/26/2018', 'MM/DD/YYYY')
	AND listing_id=l.id))
AND 22>=minimum_nights
AND 22<=maximum_nights
AND 1<=bedrooms
AND 2<=beds
AND 'Harlem'=neighborhood;

-------------------------------------------------------------------
/*Test5: Test neighborhood
Listings should change from those in Test1 due to changing neighborhood.
Listings should still match the other criteria from Test1
*/

SELECT DISTINCT id, listing_url
FROM Listing AS l, Offering
WHERE accommodates>=3
AND guests_included<=3
AND 5=(SELECT COUNT(*)
	FROM Offering
	WHERE date_for_stay<=to_date('07/25/2019', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('07/21/2019', 'MM/DD/YYYY')
	AND available='t'
	AND listing_id=l.id)
AND 300::MONEY<=(((3-guests_included)*extra_people*5)::MONEY + (SELECT SUM(price)
	FROM Offering
	WHERE date_for_stay<=to_date('07/25/2019', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('07/21/2019', 'MM/DD/YYYY')
	AND listing_id=l.id))
AND 900::MONEY>=(((3-guests_included)*extra_people*5)::MONEY + (SELECT SUM(price)
	FROM Offering
	WHERE date_for_stay<=to_date('07/25/2019', 'MM/DD/YYYY')
	AND date_for_stay>=to_date('07/21/2019', 'MM/DD/YYYY')
	AND listing_id=l.id))
AND 5>=minimum_nights
AND 5<=maximum_nights
AND 1<=bedrooms
AND 2<=beds
AND 'Park Slope'=neighborhood;

-------------------------------------------------------------------