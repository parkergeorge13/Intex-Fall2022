from django.shortcuts import render
import requests, json

from kidney_app.models import Food, Account

# Create your views here.
def landingPageView(request):
    return render(request, 'kidney_app/landing.html')

def indexPageView(request) :
    if request.method == 'POST':
        account = Account()

        account.first_name = request.POST['first_name']
        account.last_name = request.POST['last_name']
        account.gender = request.POST['gender']
        account.birth_date = request.POST['birth_date']
        account.height = request.POST['height']
        account.weight = request.POST['weight']
        account.condition = request.POST['condition']
        account.username = request.POST['username']
        account.password = request.POST['password']

        account.save()

        return trackerPageView(request)
        
    else :
        return render(request, 'kidney_app/index.html')

def trackerPageView(request):
    return render(request, 'kidney_app/tracker.html')

def displayFoodPageView(request):
    data = Food.objects.all()

    context = {
        'food' : data
    } 
    return render(request, 'kidney_app/displayFood.html', context)

def searchFoodPageView(request):
    return render(request, 'kidney_app/searchFood.html')

def deleteFoodPageView(request, id) :
    data = Food.objects.get(id = id)

    data.delete()

    return displayFoodPageView(request)

def createFoodPageView(request):
    if request.method == 'POST':
        food = Food()

        food.food_desc = request.POST['food_desc']

        food.save()

        return displayFoodPageView(request)
        
    else :
        return render(request, 'kidney_app/createFood.html')

def editFoodPageView(request) :
    if request.method == 'POST':
        id = request.POST['id']

        food = Food.objects.get(id=id)

        food.food_desc = request.POST['food_desc']

        food.save()

        return displayFoodPageView(request)

def editSingleFoodPageView(request, id):
    data = Food.objects.get(id = id)

    context = {
        'food' : data
    } 
    return render(request, 'kidney_app/editFood.html', context)