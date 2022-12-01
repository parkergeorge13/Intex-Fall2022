from django.urls import path, re_path
from .views import indexPageView, trackerPageView, searchFoodPageView, createFoodPageView, landingPageView, displayFoodPageView, deleteFoodPageView, editFoodPageView, editSingleFoodPageView, search_food, sign_in
from kidney_app import views

urlpatterns = [
    path("", landingPageView, name="landing"),
    path("display_login_results", sign_in, name="sign_in"),
    path("/index", indexPageView, name="index"),
    path("/tracker", trackerPageView, name="tracker"),
    path("/displayFood", displayFoodPageView, name="displayFood"),
    path("/searchFood", searchFoodPageView, name="searchFood"),
    path("/createFood/", createFoodPageView, name="createFood"),
    path("display_search_results", search_food, name="search_food"),
    path("/deleteFood/<int:id>/" , deleteFoodPageView, name="deleteFood"),
    path("/editFood/" , editFoodPageView, name="editFood"),
    path("/displayFood/<int:id>/" , editSingleFoodPageView, name="editSingleFood"),
    
]