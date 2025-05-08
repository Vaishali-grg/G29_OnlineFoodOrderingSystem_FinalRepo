from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
import requests

API_BASE_URL = 'http://127.0.0.1:5000/api/recipes'

def recipe_list(request):
    response = requests.get(API_BASE_URL)
    if response.status_code == 200:
        recipes = response.json()
    else:
        recipes = []
    return render(request, 'frontend/recipe_list.html', {'recipes': recipes})

def recipe_create(request):
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'ingredients': request.POST.get('ingredients', '').split('\n'),
            'instructions': request.POST.get('instructions', '')
        }
        response = requests.post(API_BASE_URL, json=data)
        if response.status_code == 201:
            return redirect('recipe_list')
    
    return render(request, 'frontend/recipe_form.html', {'form_action': 'create'})

def recipe_update(request, recipe_id):
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'ingredients': request.POST.get('ingredients', '').split('\n'),
            'instructions': request.POST.get('instructions', '')
        }
        response = requests.put(f"{API_BASE_URL}/{recipe_id}", json=data)
        if response.status_code == 200:
            return redirect('recipe_list')
    
    # GET request - fetch existing recipe
    response = requests.get(f"{API_BASE_URL}/{recipe_id}")
    if response.status_code == 200:
        recipe = response.json()
        # Convert ingredients list to newline-separated string for textarea
        recipe['ingredients'] = '\n'.join(recipe['ingredients'])
        return render(request, 'frontend/recipe_form.html', {
            'recipe': recipe,
            'form_action': 'update',
            'recipe_id': recipe_id
        })
    return redirect('recipe_list')

def recipe_delete(request, recipe_id):
    if request.method == 'POST':
        response = requests.delete(f"{API_BASE_URL}/{recipe_id}")
    return redirect('recipe_list')

# frontend/views.py
def recipe_list_readonly(request):
    response = requests.get(API_BASE_URL)
    if response.status_code == 200:
        recipes = response.json()
    else:
        recipes = []
    return render(request, 'frontend/recipe_list_readonly.html', {'recipes': recipes})