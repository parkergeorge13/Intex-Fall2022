from django.urls import path, re_path
from .views import indexPageView, trackerPageView, searchFoodPageView, createFoodPageView, landingPageView, displayFoodPageView, deleteFoodPageView, editFoodPageView, editSingleFoodPageView, search_food, tracker_date_meal
from kidney_app import views

urlpatterns = [
    path("", landingPageView, name="landing"),
    path("/index", indexPageView, name="index"),
    path("/tracker", trackerPageView, name="tracker"),
    path("/tracker_date_meal", tracker_date_meal, name="tracker_date_meal"),
    path("/displayFood", displayFoodPageView, name="displayFood"),
    path("/searchFood", searchFoodPageView, name="searchFood"),
    path("/createFood/", createFoodPageView, name="createFood"),
    path("display_search_results", search_food, name="search_food"),
    path("/deleteFood/<int:id>/" , deleteFoodPageView, name="deleteFood"),
    path("/editFood/" , editFoodPageView, name="editFood"),
    path("/displayFood/<int:id>/" , editSingleFoodPageView, name="editSingleFood"),
]