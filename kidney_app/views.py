from django.shortcuts import render

# Create your views here.
def indexPageView(request) :
    return render(request, 'kidney_app/index.html')

def trackerPageView(request):
    return render(request, 'kidney_app/tracker.html')

def searchFoodPageView(request):
    return render(request, 'kidney_app/searchFood.html')

def createFoodPageView(request):
    return render(request, 'kidney_app/createFood.html')