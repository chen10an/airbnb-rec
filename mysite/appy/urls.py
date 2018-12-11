from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
	path('', views.home),
	path('customize', views.customize),
	path('load', views.load),
	path('listing', views.listing),
	path('nolisting', views.nolisting),
	path('tryagain', views.home)
]
