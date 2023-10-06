from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Cheese

class CheeseListView(ListView):
    model = Cheese
