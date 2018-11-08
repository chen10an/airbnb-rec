import xlrd
import psycopg2

# conn = psycopg2.connect("dbname=airbnbsmall user=postgres password=#Fang2016")
conn = psycopg2.connect("dbname=airbnb user=postgres password=#Fang2016")
cur = conn.cursor()


wb = xlrd.open_workbook('listings.xlsx') 
# wb = xlrd.open_workbook('listingsmall.xlsx') 
# wb = xlrd.open_workbook('Hello.xlsx') 

sheet = wb.sheet_by_index(0) 

for i in range (1, sheet.nrows):
# for i in range (1, 20):
	idnum = sheet.cell_value(i,0)
	url = sheet.cell_value(i,1)
	name = sheet.cell_value(i,4)
	description = sheet.cell_value(i, 7)
	accommodates = sheet.cell_value(i, 53)
	guests = sheet.cell_value(i, 65)
	extraPeople = sheet.cell_value(i, 66)
	bedrooms = sheet.cell_value(i, 55)
	bed = sheet.cell_value(i, 56)
	neighborhood = sheet.cell_value(i, 39)
	latitude = sheet.cell_value(i, 48)
	longitude = sheet.cell_value(i, 49)
	minNights = sheet.cell_value(i, 67)
	maxNights = sheet.cell_value(i, 68)

	if(sheet.cell_type(i, 55) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK)):
		bedrooms = None
	if(sheet.cell_type(i, 56) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK)):
		bed = None
	cur.execute("""INSERT INTO listing VALUES (%s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (idnum, url, name, description, accommodates, guests, extraPeople, bedrooms, bed, neighborhood, latitude, longitude, minNights, maxNights))

conn.commit()

cur.close()
conn.close()

#DELETE FROM Listing WHERE id in (SELECT id FROM Listing);  #use to delete all rows in Listing