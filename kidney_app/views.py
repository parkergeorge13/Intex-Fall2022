from django.shortcuts import render
from kidney_app.models import Food, Account, Nutrient
from kidney_app.api import *
from kidney_app.models import Food, Account, Nutrient
from django.db import connection

# HOW TO EXECUTE A SQL STATEMENT
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM kidney_app_food as f INNER JOIN kidney_app_nutrient as je ON f.id = je.id")
# rows = cursor.fetchall()
# print(rows)

global_test = ''
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
        for i in data:
            if str(i) == username + ' ' + password:
                un_check.append(True)

        # If there are duplicates
        if True in un_check:
            global global_test 
            global_test = username
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
        "meals" : ["Breakfast", "Lunch", "Dinner", "Snack", "Water"],
        'test' : global_test
    }
    return render(request, 'kidney_app/tracker.html', context)

def tracker_date_meal(request):
    if request.method == 'POST':
        mealName = request.POST.get('mealName')
        if mealName == 'Water':
            return render(request, 'kidney_app/water.html')
    context = {
        'mealName': mealName
    }
    return render(request, 'kidney_app/displayFood.html', context)

def createWaterPageView(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))

        nutrient = Nutrient()
        nutrient.water = amount

        nutrient.save()

    return render(request, 'kidney_app/displayFood.html')

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
        nutrient = Nutrient()

        food.food_desc = request.POST['food']
        nutrient.sodium = request.POST['nutrients_0']
        nutrient.protein = request.POST['nutrients_1']
        nutrient.potassium = request.POST['nutrients_2']
        nutrient.phosphorus = request.POST['nutrients_3']

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
    context = {
        "food" : food,
        'nutrients' : nutrition(food)
    }
    
    return render(request, 'kidney_app/searchFood.html', context)            