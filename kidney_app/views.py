from django.shortcuts import render

# Create your views here.
def landingPageView(request):
    return render(request, 'kidney_app/landing.html')

def indexPageView(request) :
    return render(request, 'kidney_app/index.html')

def trackerPageView(request):
    return render(request, 'kidney_app/tracker.html')

def displayFoodPageView(request):
    return render(request, 'kidney_app/displayFood.html')

def searchFoodPageView(request):
    return render(request, 'kidney_app/searchFood.html')

def createFoodPageView(request):
    return render(request, 'kidney_app/createFood.html')

def search_food(request):
    if request.method == 'POST':
        food = request.POST.get('search')
    context = {
        "food" : food
    }
    return render(request, 'kidney_app/searchFood.html', context)            

