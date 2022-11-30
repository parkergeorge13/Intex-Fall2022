from django.urls import path, re_path
from .views import indexPageView, trackerPageView, searchFoodPageView, createFoodPageView, landingPageView, displayFoodPageView, search_food
from kidney_app import views

urlpatterns = [
    path("", landingPageView, name="landing"),
    path("/createAccount", indexPageView, name="index"),
    path("/tracker", trackerPageView, name="tracker"),
    path("/displayFood", displayFoodPageView, name="displayFood"),
    path("/searchFood", searchFoodPageView, name="searchFood"),
    path("/createFood", createFoodPageView, name="createFood"),
    path("display_search_results", search_food, name="search_food")
]