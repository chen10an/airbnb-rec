--Create tables for listings and the dates they are available
CREATE TABLE Listing
(id INTEGER NOT NULL PRIMARY KEY,
match_score REAL,
listing_url TEXT NOT NULL,
name TEXT NOT NULL,
description TEXT NOT NULL,
accommodates INTEGER NOT NULL,
guests_included INTEGER NOT NULL,
extra_people INTEGER NOT NULL,
bedrooms INTEGER,
beds INTEGER,
neighborhood TEXT NOT NULL,
latitude REAL NOT NULL,
longitude REAL NOT NULL,
minimum_nights INTEGER NOT NULL,
maximum_nights INTEGER NOT NULL);

CREATE TABLE Offering
(listing_id INTEGER NOT NULL REFERENCES Listing(id) ON DELETE CASCADE ON UPDATE CASCADE,
date_for_stay DATE NOT NULL,
available CHAR(1) NOT NULL CHECK (available='t' OR available='f'),
price MONEY,
PRIMARY KEY(listing_id, date_for_stay));

CREATE TABLE Business
(id TEXT NOT NULL,
weight REAL,
name TEXT NOT NULL,
url TEXT NOT NULL,
price TEXT CHECK (price='$' OR price='$$' OR price='$$$' OR price='$$$$' OR price=NULL),
rating REAL NOT NULL,
latitude REAL NOT NULL,
longitude REAL NOT NULL,
category TEXT NOT NULL,
PRIMARY KEY(id, category));
-------------------------------------------------------------------
--Create triggers for inserts, updates, and deletes
CREATE FUNCTION TF_ListingIdAlreadyExists() RETURNS TRIGGER AS $$
BEGIN
IF(NEW.id IN (SELECT id FROM Listing)) THEN
	RAISE EXCEPTION 'Listing id already taken';
END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_ListingIdAlreadyExists
	BEFORE INSERT OR UPDATE OF id ON Listing
	FOR EACH ROW
	EXECUTE PROCEDURE TF_ListingIdAlreadyExists();