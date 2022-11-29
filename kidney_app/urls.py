from django.urls import path
from .views import indexPageView, trackerPageView, searchFoodPageView, createFoodPageView, landingPageView

urlpatterns = [
    path("", landingPageView, name="landing"),
    path("/createAccount", indexPageView, name="index"),
    path("/tracker", trackerPageView, name="tracker"),
    path("/searchFood", searchFoodPageView, name="searchFood"),
    path("/createFood", createFoodPageView, name="createFood")
]