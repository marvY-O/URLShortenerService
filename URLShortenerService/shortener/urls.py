from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('shorten/', views.shorten),
    path('<str:shortID>/', views.retrieve_url_test.as_view()), #use retrieve_url for deployment purpose, retrieve_url_test is only for testing
]