from django.db import models
from datetime import datetime

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    gender = models.CharField(max_length=25)
    birth_date = models.DateField(default=datetime.today, blank=True)
    height = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    condition = models.CharField(max_length=25)

    def __str__(self):
        return (self.username)
class Journal_Entry(models.Model):
    date = models.DateField(default=datetime.today, blank=True)
    meal_category = models.CharField(max_length=25)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return (self.food_desc)

class Food(models.Model):
    food_desc = models.CharField(max_length=25)
    journal_entry = models.ManyToManyField(Journal_Entry, blank=True)
    def __str__(self):
        return (self.food_desc)

class Nutrient(models.Model):
    sodium = models.IntegerField(default=0)
    protein = models.IntegerField(default=0) 
    water = models.IntegerField(default=0)
    potassium = models.IntegerField(default=0)
    phosphorus = models.IntegerField(default=0)
    food = models.ManyToManyField(Food, blank=True)

    def __str__(self):
        return (self.food)
