from django.urls import path
from .views import indexPageView, trackerPageView, searchFoodPageView, createFoodPageView, landingPageView, displayFoodPageView, deleteFoodPageView, editFoodPageView, editSingleFoodPageView

urlpatterns = [
    path("", landingPageView, name="landing"),
    path("/index", indexPageView, name="index"),
    path("/tracker", trackerPageView, name="tracker"),
    path("/displayFood", displayFoodPageView, name="displayFood"),
    path("/searchFood", searchFoodPageView, name="searchFood"),
    path("/createFood/", createFoodPageView, name="createFood"),
    path("/deleteFood/<int:id>/" , deleteFoodPageView, name="deleteFood"),
    path("/editFood/" , editFoodPageView, name="editFood"),
    path("/displayFood/<int:id>/" , editSingleFoodPageView, name="editSingleFood"),
    
]