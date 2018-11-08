import datetime
import xlrd
import psycopg2

# conn = psycopg2.connect("dbname=airbnbsmall user=postgres password=#Fang2016")
conn = psycopg2.connect("dbname=airbnb user=postgres password=#Fang2016")
cur = conn.cursor()

wb = xlrd.open_workbook('calendar.xlsx') 
# wb = xlrd.open_workbook('smolcal.xlsx') 

sheet = wb.sheet_by_index(0) 

for i in range (1, sheet.nrows):
# for i in range (1, 6936):
	listingID = sheet.cell_value(i,0)
	datefloat = sheet.cell_value(i,1)
	date = datetime.datetime(*xlrd.xldate_as_tuple(datefloat, wb.datemode))
	availability = sheet.cell_value(i,2)
	price = sheet.cell_value(i, 3)

	if(sheet.cell_type(i, 3) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK)):
		price=None

	cur.execute("""INSERT INTO Offering VALUES (%s, %s, %s, %s);""", (listingID, date, availability, price))

conn.commit()

cur.close()
conn.close()