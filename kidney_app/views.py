from django.shortcuts import render
from kidney_app.models import Food, Account, Nutrient, Journal_Entry
from kidney_app.api import *
from django.db import connection
import datetime as dt

# HOW TO EXECUTE A SQL STATEMENT
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM kidney_app_food as f INNER JOIN kidney_app_nutrient as je ON f.id = je.id")
# rows = cursor.fetchall()
# print(rows)

glo_acc_pk = 0
glo_date = ''
glo_meal = ''
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
            # get the user's pk id and store it in a global variable
            cursor = connection.cursor()
            cursor.execute(f"SELECT id FROM kidney_app_account AS a WHERE a.username = '{username}'")
            rows = cursor.fetchone()
            acc = rows[0]
            global acc_pk 
            acc_pk = acc
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
    }
    return render(request, 'kidney_app/tracker.html', context)

def tracker_date_meal(request):
    if request.method == 'POST':
        mealName = request.POST.get('mealName')
        mealDate = request.POST.get('mealDate')

        context = {
            'mealName': mealName,
            'meal_date' : mealDate
        }
        global glo_date 
        glo_date = mealDate
        global glo_meal
        glo_meal = mealName
        if mealName == 'Water':
            return render(request, 'kidney_app/water.html', context)

    return render(request, 'kidney_app/displayFood.html', context)

def createWaterPageView(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        # Get date in date format to put in database
        date_raw = request.POST.get('date')
        date_list = date_raw.split('-')
        date_final = dt.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))

        #add to journal entry
        account = Account.objects.get(pk=acc_pk)
        d = Journal_Entry(date=date_final, meal_category = 'water')
        d.account = account
        d.save()

        #add to food
        a = Food(food_desc='water', )
        a.save()
        
        #add to journal entry and food
        a.journal_entry.add(d)

        #add to nutrient
        b = Nutrient(water=amount)
        b.save()
        
        #combine food and nutrient id's 
        b.food.add(a)

    return render(request, 'kidney_app/displayFood.html')

def displayFoodPageView(request):
    data = Food.objects.all()
    servings=1

    context = {
        'food' : data,
        'mealName': glo_meal,
        'meal_date' : glo_date,
        'servings': servings,
    } 

    if request.method == 'POST':
        return render(request, 'kidney_app/searchFood.html', context)

    return render(request, 'kidney_app/displayFood.html', context)

def searchFoodPageView(request):
    servings = 1 
    context = {
        "servings": servings,
        'meal_date' : glo_date,
        'mealName' : glo_meal
    }
    return render(request, 'kidney_app/searchFood.html', context)

def deleteFoodPageView(request, id) :
    data = Food.objects.get(id = id)

    data.delete()

    return displayFoodPageView(request)

def createFoodPageView(request):
    if request.method == 'POST':
        
        food_name = request.POST['food']
        sodium = request.POST['nutrients_0']
        protein = request.POST['nutrients_1']
        potassium = request.POST['nutrients_2']
        phosphorus = request.POST['nutrients_3']
        servings = request.POST['servings']

        mealName = glo_meal
        # Get date in date format to put in database
        date_raw = glo_date
        date_list = date_raw.split('-')
        date_final = dt.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))

        #add to journal entry
        account = Account.objects.get(pk=acc_pk)
        d = Journal_Entry(date=date_final, meal_category = mealName)
        d.account = account
        d.save()

        #add to food
        a = Food(food_desc=food_name)
        a.save()
        
        #add to journal entry and food
        a.journal_entry.add(d)

        #add to nutrient
        b = Nutrient(sodium=sodium, protein=protein, potassium=potassium, phosphorus=phosphorus, servings = servings)
        b.save()
        
        #combine food and nutrient id's 
        b.food.add(a)

        date = glo_date

        # sodium
        cursor = connection.cursor()
        cursor.execute(f"SELECT SUM(nutrient.sodium)as sodium FROM kidney_app_food food JOIN kidney_app_nutrient_food as nf ON nf.food_id = food.id JOIN kidney_app_nutrient as nutrient ON nf.nutrient_id = nutrient.id JOIN kidney_app_food_journal_entry as fje ON fje.food_id = food.id JOIN kidney_app_journal_entry as journal ON fje.journal_entry_id = journal.id GROUP BY journal.date HAVING journal.date = '{date}';")
        sodium = cursor.fetchone()
        totalSodium = sodium[0]

        # protein
        cursor = connection.cursor()
        cursor.execute(f"SELECT SUM(nutrient.protein)as protein FROM kidney_app_food food JOIN kidney_app_nutrient_food as nf ON nf.food_id = food.id JOIN kidney_app_nutrient as nutrient ON nf.nutrient_id = nutrient.id JOIN kidney_app_food_journal_entry as fje ON fje.food_id = food.id JOIN kidney_app_journal_entry as journal ON fje.journal_entry_id = journal.id GROUP BY journal.date HAVING journal.date = '{date}';")
        protein = cursor.fetchone()
        totalProtein = protein[0]

        # potassium
        cursor = connection.cursor()
        cursor.execute(f"SELECT SUM(nutrient.potassium)as potassium FROM kidney_app_food food JOIN kidney_app_nutrient_food as nf ON nf.food_id = food.id JOIN kidney_app_nutrient as nutrient ON nf.nutrient_id = nutrient.id JOIN kidney_app_food_journal_entry as fje ON fje.food_id = food.id JOIN kidney_app_journal_entry as journal ON fje.journal_entry_id = journal.id GROUP BY journal.date HAVING journal.date = '{date}';")
        potassium = cursor.fetchone()
        totalPotassium = potassium[0]

        # phophorus
        cursor = connection.cursor()
        cursor.execute(f"SELECT SUM(nutrient.phosphorus)as phosphorus FROM kidney_app_food food JOIN kidney_app_nutrient_food as nf ON nf.food_id = food.id JOIN kidney_app_nutrient as nutrient ON nf.nutrient_id = nutrient.id JOIN kidney_app_food_journal_entry as fje ON fje.food_id = food.id JOIN kidney_app_journal_entry as journal ON fje.journal_entry_id = journal.id GROUP BY journal.date HAVING journal.date = '{date}';")
        phophorus = cursor.fetchone()
        totalPhosphorus = phophorus[0]
        
        context = {
            'totalSodium': totalSodium,
            'totalProtein': totalProtein,
            'totalPotassium': totalPotassium,
            'totalPhosphorus': totalPhosphorus,
        }

        return render(request, 'kidney_app/displayFood.html', context)
        
    else :
        return render(request, 'kidney_app/searchFood.html')

def editFoodPageView(request) :
    if request.method == 'POST':
        id = request.POST['id']

        food = Food.objects.get(id=id)

        food.food_desc = request.POST['food_desc']

        food.save()

        return render(request, 'kidney_app/displayFood.html')

def editSingleFoodPageView(request, id):
    data = Food.objects.get(id = id)

    context = {
        'food' : data
    } 
    return render(request, 'kidney_app/editFood.html', context)

def search_food(request):
    if request.method == 'POST':
        food = request.POST.get('search')
        servings = request.POST.get('servings')
        mealName = request.POST.get('mealName')
        meal_date = request.POST.get('meal_date')
    context = {
        "food" : food,
        'nutrients' : nutrition(food),
        "servings": servings,
        'mealName': mealName,
        'meal_date' : meal_date
    }
    
    return render(request, 'kidney_app/searchFood.html', context)            

def showFoodNutrientPageView(request):
    if request.method == 'POST':
        id = request.POST['id']

        food = Food.objects.get(id=id)

        food.food_desc = request.POST['food_desc']

        food.save()

        return render(request, 'kidney_app/displayFood.html')

    # cursor = connection.cursor()
    # cursor.execute("SELECT * FROM kidney_app_food as f INNER JOIN kidney_app_nutrient as je ON f.id = je.id")
    # rows = cursor.fetchall()
    # print(rows)
    # return render(request, 'kidney_app/showFoodNutrient.html')

def showFoodNutrientSingle(request, id):
    data = Food.objects.get(id = id)

    context = {
        'food' : data
    } 
    return render(request, 'kidney_app/showFoodNutrient.html', context)