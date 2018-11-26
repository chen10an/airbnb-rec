from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('top5/', views.simple),
    path('customizePage/', views.customize),
    path('topMatches/', views.match)
]