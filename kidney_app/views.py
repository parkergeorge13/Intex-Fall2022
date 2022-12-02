from django.shortcuts import render
from kidney_app.models import Food, Account, Nutrient, Journal_Entry
from kidney_app.api import *
from django.db import connection
import datetime as dt
#generating graphs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import seaborn as sns
import psycopg2 as pg2
import pandas as pd

# HOW TO EXECUTE A SQL STATEMENT
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM kidney_app_food as f INNER JOIN kidney_app_nutrient as je ON f.id = je.id")
# rows = cursor.fetchall()
# print(rows)

acc_pk = 0
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
            cursor.close()
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
    data = Food.objects.all()
    context = {
        'food': data,
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

    return searchFoodDisplayPageView(request)

def displayFoodPageView(request):
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
    showGraph(glo_date)
    
    data = Food.objects.filter(journal_entry__date = glo_date, journal_entry__account_id = acc_pk)

    servings=1

    context = {
        'food' : data,
        'mealName': glo_meal,
        'meal_date' : glo_date,
        'servings': servings,      
    } 

    return render(request, 'kidney_app/displayFood.html', context)

def searchFoodPageView(request):
    servings = 1 
    leveltype = "Actual"
    context = {
        "servings": servings,
        'meal_date' : glo_date,
        'mealName' : glo_meal,
        'leveltype' : leveltype
    }
    return render(request, 'kidney_app/searchFood.html', context)

def searchFoodDisplayPageView(request): 
    data = Food.objects.filter(journal_entry__date = glo_date, journal_entry__account_id = acc_pk)

    servings=1

    context = {
        'food' : data,
        'mealName': glo_meal,
        'meal_date' : glo_date,
        'servings': servings,
        'totalSodium': totalSodium,
        'totalProtein': totalProtein,
        'totalPotassium': totalPotassium,
        'totalPhosphorus': totalPhosphorus,
        'weightValue': weightValue
    } 

    return render(request, 'kidney_app/displayFood.html', context)


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
        leveltype = request.POST['leveltype']

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
        b = Nutrient(sodium=sodium, protein=protein, potassium=potassium, phosphorus=phosphorus,leveltype=leveltype, servings = servings)
        b.save()
        
        #combine food and nutrient id's 
        b.food.add(a)

        date = glo_date

        # sodium
        cursor = connection.cursor()
        cursor.execute(f"SELECT SUM(nutrient.sodium)as sodium FROM kidney_app_food food JOIN kidney_app_nutrient_food as nf ON nf.food_id = food.id JOIN kidney_app_nutrient as nutrient ON nf.nutrient_id = nutrient.id JOIN kidney_app_food_journal_entry as fje ON fje.food_id = food.id JOIN kidney_app_journal_entry as journal ON fje.journal_entry_id = journal.id GROUP BY journal.date HAVING journal.date = '{date}';")
        sodium = cursor.fetchone()
        totalsodium = sodium[0]

        # protein
        cursor = connection.cursor()
        cursor.execute(f"SELECT SUM(nutrient.protein)as protein FROM kidney_app_food food JOIN kidney_app_nutrient_food as nf ON nf.food_id = food.id JOIN kidney_app_nutrient as nutrient ON nf.nutrient_id = nutrient.id JOIN kidney_app_food_journal_entry as fje ON fje.food_id = food.id JOIN kidney_app_journal_entry as journal ON fje.journal_entry_id = journal.id GROUP BY journal.date HAVING journal.date = '{date}';")
        protein = cursor.fetchone()
        totalprotein = protein[0]

        # potassium
        cursor = connection.cursor()
        cursor.execute(f"SELECT SUM(nutrient.potassium)as potassium FROM kidney_app_food food JOIN kidney_app_nutrient_food as nf ON nf.food_id = food.id JOIN kidney_app_nutrient as nutrient ON nf.nutrient_id = nutrient.id JOIN kidney_app_food_journal_entry as fje ON fje.food_id = food.id JOIN kidney_app_journal_entry as journal ON fje.journal_entry_id = journal.id GROUP BY journal.date HAVING journal.date = '{date}';")
        potassium = cursor.fetchone()
        totalpotassium = potassium[0]

        # phophorus
        cursor = connection.cursor()
        cursor.execute(f"SELECT SUM(nutrient.phosphorus)as phosphorus FROM kidney_app_food food JOIN kidney_app_nutrient_food as nf ON nf.food_id = food.id JOIN kidney_app_nutrient as nutrient ON nf.nutrient_id = nutrient.id JOIN kidney_app_food_journal_entry as fje ON fje.food_id = food.id JOIN kidney_app_journal_entry as journal ON fje.journal_entry_id = journal.id GROUP BY journal.date HAVING journal.date = '{date}';")
        phophorus = cursor.fetchone()
        totalphosphorus = phophorus[0]

        cursor = connection.cursor()
        cursor.execute(f"SELECT weight from kidney_app_account;")
        weight = cursor.fetchone()
        weightvalue = weight[0]

        global totalSodium 
        totalSodium = totalsodium
        global totalProtein 
        totalProtein = totalprotein
        global totalPotassium 
        totalPotassium = totalpotassium
        global totalPhosphorus 
        totalPhosphorus = totalphosphorus
        global weightValue 
        weightValue = weightvalue
        
        context = {
            'totalSodium': totalSodium,
            'totalProtein': totalProtein,
            'totalPotassium': totalPotassium,
            'totalPhosphorus': totalPhosphorus,
            'weightValue': weightValue
        }

        return searchFoodDisplayPageView(request)   
    else :
        return render(request, 'kidney_app/searchFood.html')

def editFoodPageView(request) :
    if request.method == 'POST':
        id = request.POST['id']

        food = Food.objects.get(id=id)

        food.food_desc = request.POST['food_desc']

        food.save()

    return searchFoodDisplayPageView(request)

def editSingleFoodPageView(request, id):
    data = Food.objects.get(id = id)
    food = data
    context = {
        'food' : data,
        'nutrients' : nutrition(food),
    } 
    return render(request, 'kidney_app/editFood.html', context)

def displayFoodAfterEdit(request):
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
    showGraph(glo_date)
    
    data = Food.objects.filter(journal_entry__date = glo_date, journal_entry__account_id = acc_pk)

    servings=1

    context = {
        'food' : data,
        'mealName': glo_meal,
        'meal_date' : glo_date,
        'servings': servings,      
    } 

    return render(request, 'kidney_app/displayFood.html', context)


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
    global acc_pk
    cursor = connection.cursor()
    cursor.execute(
        "SELECT f.food_desc, sodium, protein, potassium, phosphorus, servings FROM kidney_app_account as a"
        + " inner join kidney_app_journal_entry as je on a.id = je.account_id"
        + " inner join kidney_app_food_journal_entry as fje on je.id = fje.journal_entry_id"
        + " inner join kidney_app_food as f on fje.food_id = f.id"
        + " inner join kidney_app_nutrient_food as nf on f.id = nf.food_id"
        + " inner join kidney_app_nutrient as n on nf.nutrient_id = n.id"
        + f" where a.id = {acc_pk} and f.id = {id}"
        )
    rows = cursor.fetchall()
    context = {
        'food' : rows[0][0],
        'sodium' : rows[0][1],
        'protein' : rows[0][2],
        'potassium' : rows[0][3],
        'phosphorus' : rows[0][4],
        'servings' : rows[0][5]
        
    } 
    cursor.close()
    return render(request, 'kidney_app/showFoodNutrient.html', context)

def showGraph(date):
    #connecting to postgres
    #sodium df
    conn = pg2.connect(database='intex',
                    user='postgres',
                    password='admin')
    cur = conn.cursor()

    cur.execute(f'''SELECT 'sodium' AS nutrienttype, SUM(n.sodium) AS nutrientlevel, n.leveltype
    FROM kidney_app_nutrient as n 
	INNER JOIN kidney_app_nutrient_food as nf on n.id = nf.nutrient_id
    INNER JOIN kidney_app_food as f ON nf.food_id = f.id
	INNER JOIN kidney_app_food_journal_entry as fje ON f.id = fje.food_id
    INNER JOIN kidney_app_journal_entry as je ON je.id = fje.journal_entry_id
    WHERE date = '{date}' GROUP BY je.date, n.leveltype''')
    data = cur.fetchall()

    cols = []
    for elt in cur.description:
        cols.append(elt[0])
        
    act_sodium_df = pd.DataFrame(data=data,columns=cols)
    conn.close()

    #potassium df
    conn = pg2.connect(database='intex',
                    user='postgres',
                    password='admin')
    cur = conn.cursor()

    cur.execute(f'''SELECT 'potassium' AS nutrienttype, SUM(n.potassium) AS nutrientlevel, n.leveltype
    FROM kidney_app_nutrient as n 
	INNER JOIN kidney_app_nutrient_food as nf on n.id = nf.nutrient_id
    INNER JOIN kidney_app_food as f ON nf.food_id = f.id
	INNER JOIN kidney_app_food_journal_entry as fje ON f.id = fje.food_id
    INNER JOIN kidney_app_journal_entry as je ON je.id = fje.journal_entry_id
    WHERE date = '{date}' 
	GROUP BY je.date, n.leveltype''')
    data = cur.fetchall()

    cols = []
    for elt in cur.description:
        cols.append(elt[0])
        
    act_potassium_df = pd.DataFrame(data=data,columns=cols)
    conn.close()
    
    #phosphorus df
    conn = pg2.connect(database='intex',
                    user='postgres',
                    password='admin')
    cur = conn.cursor()

    cur.execute(f'''SELECT 'phosphorus' AS nutrienttype, SUM(n.phosphorus) AS nutrientlevel, n.leveltype
    FROM kidney_app_nutrient as n 
	INNER JOIN kidney_app_nutrient_food as nf on n.id = nf.nutrient_id
    INNER JOIN kidney_app_food as f ON nf.food_id = f.id
	INNER JOIN kidney_app_food_journal_entry as fje ON f.id = fje.food_id
    INNER JOIN kidney_app_journal_entry as je ON je.id = fje.journal_entry_id
    WHERE date = '{date}' 
    GROUP BY je.date, n.leveltype''')
    data = cur.fetchall()

    cols = []
    for elt in cur.description:
        cols.append(elt[0])
        
    act_phosphorus_df = pd.DataFrame(data=data,columns=cols)
    conn.close()

    #protein df
    conn = pg2.connect(database='intex',
                    user='postgres',
                    password='admin')
    cur = conn.cursor()

    cur.execute(f'''SELECT 'protein' AS nutrienttype, SUM(n.protein) AS nutrientlevel, n.leveltype
    FROM kidney_app_nutrient as n 
	INNER JOIN kidney_app_nutrient_food as nf on n.id = nf.nutrient_id
    INNER JOIN kidney_app_food as f ON nf.food_id = f.id
	INNER JOIN kidney_app_food_journal_entry as fje ON f.id = fje.food_id
    INNER JOIN kidney_app_journal_entry as je ON je.id = fje.journal_entry_id
    WHERE date = '{date}'
    GROUP BY je.date, n.leveltype''')
    data = cur.fetchall()

    cols = []
    for elt in cur.description:
        cols.append(elt[0])
        
    act_protein_df = pd.DataFrame(data=data,columns=cols)
    conn.close()

    #water df
    conn = pg2.connect(database='intex',
                    user='postgres',
                    password='admin')
    cur = conn.cursor()

    cur.execute(f'''SELECT 'water' AS nutrienttype, SUM(n.water) AS nutrientlevel, n.leveltype
    FROM kidney_app_nutrient as n 
	INNER JOIN kidney_app_nutrient_food as nf on n.id = nf.nutrient_id
    INNER JOIN kidney_app_food as f ON nf.food_id = f.id
	INNER JOIN kidney_app_food_journal_entry as fje ON f.id = fje.food_id
    INNER JOIN kidney_app_journal_entry as je ON je.id = fje.journal_entry_id
    WHERE date = '{date}'
    GROUP BY je.date, n.leveltype''')
    data = cur.fetchall()

    cols = []
    for elt in cur.description:
        cols.append(elt[0])
    act_water_df = pd.DataFrame(data=data,columns=cols)

    # postgres graph test
    # import numpy as np
    # import pandas as pd
    # import matplotlib.pyplot as plt
    # import seaborn as sns

    # sns.barplot(x = 'nutrienttype', y = 'nutrientlevel', hue = 'leveltype', data = potassium_df)

    # plt.title('Postgres Test')
    # plt.savefig('static/img/test.jpg')
    # plt.savefig('intex/static/img/test.jpg')

    # nutrientList3 = ['Water']


    #creating a dataframe for suggested values
    #micro df
    data=[['sodium', 1898, 'suggested'], ['potassium', 2750, 'suggested'], ['phosphorus', 900, 'suggested']]

    suggested_micro_df = pd.DataFrame(data, 
                    index=[1, 2, 3], 
                    columns=['nutrienttype', 'nutrientlevel', 'leveltype'])

    suggested_micro_df.index.names = ['NutrientID']
    suggested_micro_df

    #macro df
    data=[['protein', 0.6, 'suggested']]

    suggested_macro_df = pd.DataFrame(data, 
                    index=[1], 
                    columns=['nutrienttype', 'nutrientlevel', 'leveltype'])

    suggested_macro_df.index.names = ['NutrientID']
    suggested_macro_df

    #water df
    data=[['water', 3700, 'suggested']]

    suggested_water_df = pd.DataFrame(data, 
                    index=[1], 
                    columns=['nutrienttype', 'nutrientlevel', 'leveltype'])

    suggested_water_df.index.names = ['NutrientID']
    suggested_water_df

    #concat dfs
    microframes = [act_sodium_df, act_potassium_df, act_phosphorus_df, suggested_micro_df]
    microResult = pd.concat(microframes)

    macroframes = [act_protein_df, suggested_macro_df]
    macroResult = pd.concat(macroframes)

    waterframes = [act_water_df, suggested_water_df]
    waterResult = pd.concat(waterframes)

    # nutrientList1 = ['sodium', 'potassium', 'phosphorus']

    # micro_df = microResult[(microResult['nutrienttype'].isin(nutrientList1))]

    # we will have a "nutrient type" column that has each of the 5 nutrient names
    # we will have a "nutrient level" column that has an integer of the amount of that nutrient
    # we will have a "level type" column that specifies whether that row is a "suggested" level from the database or a recording of their "actual" level
    sns.barplot(x = 'nutrienttype', y = 'nutrientlevel', hue = 'leveltype', data = microResult)

    plt.title('Daily Micronutrients (miligrams)')
    plt.savefig('static/img/micro.jpg')
    plt.savefig('intex/static/img/micro.jpg')

    nutrientList2 = ['protein']

    macro_df = macroResult[(macroResult['nutrienttype'].isin(nutrientList2))]

    sns.barplot(x = 'nutrienttype', y = 'nutrientlevel', data = macroResult)

    plt.title('Daily Macronutrients (grams)')
    plt.savefig('static/img/macro.jpg')
    plt.savefig('intex/static/img/macro.jpg')

    nutrientList3 = ['water']

    water_df = waterResult[(waterResult['nutrienttype'].isin(nutrientList3))]

    sns.barplot(x = 'nutrienttype', y = 'nutrientlevel', data = waterResult)

    plt.title('Daily Water Intake (mililiters)')
    plt.savefig('static/img/water.jpg')
    plt.savefig('intex/static/img/water.jpg')
    plt.switch_backend('agg')
    conn.close()