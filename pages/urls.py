from django.urls import path
from .views import homePage, aboutUsPage

urlpatterns = [
    path("", homePage, name="home"),
    path("about_us/", aboutUsPage, name='about_us'),
]
