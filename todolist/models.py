from django.db import models
from datetime import date
import datetime

# Create your models here.

from django.utils import timezone
class Category(models.Model): # The Category table name that inherits models.Model
    name = models.CharField(max_length=100) #Like a varchar    
    class Meta:
       verbose_name = ("category")
       verbose_name_plural = ("categories")    
    def __str__(self):
        return self.name #name to be shown when called
class TodoList(models.Model): #Todolist able name that inherits models.Model
    id = models.IntegerField(primary_key=True)
    userid = models.CharField(default='bkumar',max_length=50) # a varchar
    title = models.CharField(max_length=250) # a varchar
    content = models.TextField(blank=True) # a text field 
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
    category = models.ForeignKey(Category, default="general", on_delete=models.PROTECT) # a foreignkey    
    status = models.TextField(default="open") # a text field 
    class Meta:
        ordering = ["-created"] #ordering by the created field    
    def __str__(self):
    	return self.title #name to be shown when called

    @property
    def todays_date(self):
        return date.today()
    @property
    def tomorrows_date(self):
        return date.today() + datetime.timedelta(days=1)