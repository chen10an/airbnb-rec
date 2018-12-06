from django.db import models

# Create your models here.
class Listing(models.Model):
    id = models.IntegerField(primary_key=True)
    match_score = models.FloatField(blank=True, null=True)
    listing_url = models.TextField()
    name = models.TextField()
    description = models.TextField()
    accommodates = models.IntegerField()
    guests_included = models.IntegerField()
    extra_people = models.IntegerField()
    bedrooms = models.IntegerField(blank=True, null=True)
    beds = models.IntegerField(blank=True, null=True)
    neighborhood = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    minimum_nights = models.IntegerField()
    maximum_nights = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'listing'


class Offering(models.Model):
    listing_id = models.IntegerField(primary_key=True)
    date_for_stay = models.DateField()
    available = models.CharField(max_length=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'offering'
        unique_together = (('listing_id', 'date_for_stay'),)

class Business(models.Model):
    id = models.TextField(primary_key=True)
    weight = models.FloatField(blank=True, null=True)
    name = models.TextField()
    url = models.TextField()
    price = models.TextField(blank=True, null=True)
    rating = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    category = models.TextField()

    class Meta:
        managed = False
        db_table = 'business'
        unique_together = (('id', 'category'),)
