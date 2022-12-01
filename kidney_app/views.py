from django.shortcuts import render
import requests, json
from kidney_app.models import Food, Account, Nutrient
from kidney_app.api import *

# Create your views here.
def landingPageView(request):
    return render(request, 'kidney_app/landing.html')

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        context = {
            "username" : username,
            'password' : password,
            'duplicate' : False
        }
        data = Account.objects.all()

        #check if un and pw exist
        un_check = []
        pw_check = []
        for i in data:
            if str(i) == username + ' ' + password:
                un_check.append(True)

        # If there are duplicates
        if True in un_check:
            return trackerPageView(request)
        # If no duplicates
        else:
            context['duplicate'] = True
            return render(request, 'kidney_app/landing.html', context)

    return render(request, 'kidney_app/landing.html', context)

def indexPageView(request) :
    data = Account.objects.all()
    context = {
        'acc' : data,
        'duplicate' : False
    }

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
        
        # Don't allow duplicate users
        check = []
        for i in data:
            if str(i) == account.username:
                check.append(True)
        # If no duplicates
        if True not in check:
            account.save()
            return landingPageView(request)
        # If there are duplicates
        else:
            context['duplicate'] = True
            return render(request, 'kidney_app/index.html', context)
      
    else :
        return render(request, 'kidney_app/index.html', context)

def trackerPageView(request):
    data = Nutrient.objects.all()
    context = {
        'nutrient': data,
        "meals" : ["Breakfast", "Lunch", "Dinner", "Snack", "Water"]
    }
    return render(request, 'kidney_app/tracker.html', context)

def displayFoodPageView(request):
    data = Food.objects.all()
    # if request.method == 'POST':
    #     mealName = request.POST.get('mealName')
    #     mealDate = request.POST.get('mealDate')
    context = {
        'food' : data,
        # 'mealName': mealName,
        # 'mealDate': mealDate
    } 
    return render(request, 'kidney_app/displayFood.html', context)

def searchFoodPageView(request):
    serving = 1 
    context = {
        "serving": serving
    }
    return render(request, 'kidney_app/searchFood.html', context)

def deleteFoodPageView(request, id) :
    data = Food.objects.get(id = id)

    data.delete()

    if request.method == 'POST':
        mealName = request.POST.get('mealName')
        mealDate = request.POST.get('mealDate')
    context = {
        'mealName': mealName,
        'mealDate': mealDate
    } 

    return render(request, 'kidney_app/displayFood.html', context)

def createFoodPageView(request):
    if request.method == 'POST':
        food = Food()
        nutrient = Nutrient()

        food.food_desc = request.POST['food']
        nutrient.sodium = request.POST['nutrients_0']
        nutrient.protein = request.POST['nutrients_1']
        nutrient.potassium = request.POST['nutrients_2']
        nutrient.phosphorus = request.POST['nutrients_3']
        nutrient.serving = request.POST['serving']

        food.save()
        nutrient.save()

        return displayFoodPageView(request)
        
    else :
        return render(request, 'kidney_app/searchFood.html')

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

def search_food(request):
    if request.method == 'POST':
        food = request.POST.get('search')
        serving = request.POST.get('serving')
    context = {
        "food" : food,
        'nutrients' : nutrition(food),
        "serving": serving
    }
    
    return render(request, 'kidney_app/searchFood.html', context)   
