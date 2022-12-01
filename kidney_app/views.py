from django.shortcuts import render
<<<<<<< HEAD
import requests, json

from kidney_app.models import Food, Account, Nutrient
=======
from kidney_app.api import *
from kidney_app.models import Food, Account
>>>>>>> ae8833d8544fcc0aae5e44b09bc53a6e92af51ef

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

<<<<<<< HEAD
def nutrition(food):
    try: 
        # initial install when running the api: pip install lxml html5lib beautifulsoup4 requests 
        api_key = '70hA3deEKViqq4Q1UG7zkyUJDXk12UvOEUfe90wu'

        # API url used for many variables. 
        # response = requests.get(f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={food}")

        # API url to retrieve only one variable
        response = requests.get(f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food}&pageSize=5&api_key={api_key}")

        # if the api call throws anything other than a 200 response
        if str(response.status_code)[0] != '2':
            return None

        # Condense the response into a json variable
        body = response.json()

        # Creates the dictionary we'll store the first 5 results
        food_nutrients_dict = {}
            
        # Pulls the first 5 values for a user's food search
        for iteration in range(0, 5):
            # If the API call returns nutrition information for the food than the food and all it's information are stored in an array
            if len(body['foods']) >= iteration + 1:
                food_nutrients = body['foods'][iteration]['foodNutrients']
                serving_size = body['foods'][iteration]
                food_nutrients_pretty = json.dumps(food_nutrients, indent=4)
                serving_size_pretty = json.dumps(serving_size, indent=4)
                # print(food_nutrients_pretty)
                # the government's nutrient id's for sodium, protein, potassium, and phosphorus
                nutrients_id = [1093, 1003, 1092, 1091 ]
                nutrients_name = ['sodium', 'protein', 'potassium', 'phosphorus']
                nutrients_name_unsorted = []
                nutrients_value_unsorted = []
                nutrients_value_sorted = []

                # Extracts the 5 specific nutrients desired from the json and their values
                for i in range(0, len(food_nutrients)):
                    id = food_nutrients[i]['nutrientId']
                    for ii in range(0, len(nutrients_id)):
                        if id == nutrients_id[ii]:
                            nutrients_name_unsorted.append(nutrients_name[ii])
                            nutrients_value_unsorted.append(food_nutrients[i]['value'])

                # If one of the nutrients is not found in the data then a value of 0 is automatically assigned to that nutrient
                for i in range(0, len(nutrients_name)):
                    if nutrients_name[i] not in nutrients_name_unsorted:
                        nutrients_name_unsorted.append(nutrients_name[i])
                while len(nutrients_value_unsorted) < 4:
                    nutrients_value_unsorted.append(0)

                # Sorts the nutrients in the order that they will be inputted into their table
                for i in range(0, len(nutrients_name)):
                    for ii in range(0, len(nutrients_name)):
                        if nutrients_name[i] == nutrients_name_unsorted[ii]:
                            nutrients_value_sorted.append(nutrients_value_unsorted[ii])

                # Adds the nutrients to the dictionary
                food_nutrients_dict[iteration] = nutrients_value_sorted
        
        # Put all matching nutrients into one array
        food_nutrients_dict_sorted = {}
        for i in range(0, len(food_nutrients_dict[0])):
            sorted_nutrients = []
            for ii in range(0, len(food_nutrients_dict)):
                sorted_nutrients.append(int(food_nutrients_dict[ii][i]))
            food_nutrients_dict_sorted[i] = sorted(sorted_nutrients, key = int)

        # Output the median of all nutrients into one final dictionary (median because data is skewed)
        median_nutrients = {}
        for i in range(0, len(food_nutrients_dict_sorted)):
            median_nutrients[i] = food_nutrients_dict_sorted[i][2]
            #average_nutrients[i] = round((sum(food_nutrients_dict_sorted[i])) / (len(food_nutrients_dict_sorted[i])))
            #print(sum(food_nutrients_dict_sorted[i]))
        return median_nutrients
            
    except Exception as e:
        print('\nUnable to connect to the vending API.')
        print(e)
=======
>>>>>>> ae8833d8544fcc0aae5e44b09bc53a6e92af51ef
