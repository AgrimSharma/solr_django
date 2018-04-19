from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('add/', add_document, name='add_document'),
    path('search/', search_document, name='search_document'),
    path('search_city/', search_city_document, name='search_city_document'),
    path('university/', add_university, name='add_university'),
    path('property/', add_property, name='add_property'),
    path('city/', add_city, name='add_city'),
]
