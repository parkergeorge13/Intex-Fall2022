from django.contrib import admin
from .models import Account, Journal_Entry, Food, Nutrient

# Register your models here.
admin.site.register(Account)
admin.site.register(Journal_Entry)
admin.site.register(Food)
admin.site.register(Nutrient)