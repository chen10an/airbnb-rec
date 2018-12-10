import pandas as pd
import numpy as np
import sklearn
import sklearn.preprocessing
import re
import pickle
import psycopg2


businesses = pickle.load(open("yelp_businesses_cleaned.pickle", "rb"))

conn = psycopg2.connect("dbname=airbnb user=postgres password=#Fang2016")
cur = conn.cursor()
# for i in range(0, 481):
# 	print(businesses.iat[i, 3])
S=set()

for i in range(0, 481):
	businessID=businesses.iat[i, 0]
	name=businesses.iat[i, 1]
	url=businesses.iat[i, 2]
	price=businesses.iat[i, 3]
	rating=businesses.iat[i, 4]
	latitude=businesses.iat[i, 5]
	longitude=businesses.iat[i, 6]
	for k in range(7, 122):		
		if(businesses.iat[i, k]==1):
			category=businesses.columns[k]
			if(category=='Pasta Shops'):
				category='Italian'
			if(category=='Tapas Bars'):
				category='Tapas/Small Plates'
			businessTuple=(businessID, category)
			if businessTuple not in S:
				S.add(businessTuple)
				if(price=='nan'):
					cur.execute("""INSERT INTO business VALUES (%s, NULL, %s, NULL, %s, %s, %s, %s, %s);""", (businessID, name, url, rating, latitude, longitude, category))
				else:
					cur.execute("""INSERT INTO business VALUES (%s, NULL, %s, %s, %s, %s, %s, %s, %s);""", (businessID, name, url, price, rating, latitude, longitude, category))

conn.commit()

cur.close()
conn.close()
