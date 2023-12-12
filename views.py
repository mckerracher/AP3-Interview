from django.http import HttpResponse, JsonResponse  # used for handling API responses
from django.shortcuts import render, redirect  # used for page rendering
from django.contrib import \
    messages  # Django's messages framework provides a mechanism for passing temporary messages from the server-side  (Django views) to the client-side (templates)
import helpers  # helper functions module
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = 'https://my-api.com:8000/'


def home(request):
    template = 'App/home.html'
    logger.info('Loading home page')
    return render(request, template)


def view_all_recipes(request):
    recipes = helpers.api_get(f'{BASE_URL}recipes/')
    context = {'recipes': recipes or []}
    template = 'App/view_all_recipes.html'
    logger.info('Loading view_all_recipes page')
    return render(request, template, context)


def view_recipe(request, recipe_id):
    recipe = helpers.api_get(f'{BASE_URL}recipes/{recipe_id}')
    if request.method == 'POST':
        # the HTML input form would be a dropdown to ensure input format is correct
        new_serving_size = int(request.POST.get('new_serving_size', 1))
        original_serving_size = recipe['serving_size']
        scale_factor = new_serving_size / original_serving_size

        # Adjust ingredient quantities
        for ingredient in recipe['ingredients']:
            # Assuming ingredient quantities are numerical values
            ingredient['quantity'] *= scale_factor

        recipe['serving_size'] = new_serving_size

    context = {'recipe': recipe}
    template = 'App/view_recipe.html'
    return render(request, template, context)


def create_recipe(request):
    recipe_data_user_input = ''
    if request.method == 'POST':
        recipe_data_user_input = request.POST.get('input_field', '')
        recipe_data = helpers.recipe_data_to_json(recipe_data_user_input)

        if not helpers.api_post(f'{BASE_URL}recipes/', recipe_data):
            messages.error(request, 'Recipe creation failed, please try again.')

    context = {
        'input_field': recipe_data_user_input,
        'messages': messages.get_messages(request)
    }
    template = 'App/create_recipe.html'
    return render(request, template, context)


def edit_recipe(request, recipe_id):
    recipe_data_user_input = ''

    if request.method == 'POST':
        recipe_data_user_input = request.POST.get('input_field', '')
        updated_recipe_data = helpers.recipe_data_to_json(recipe_data_user_input)

        if not helpers.api_put(f'{BASE_URL}recipes/{recipe_id}', updated_recipe_data):
            messages.error(request, 'Recipe edit failed, please try again.')

    recipe = helpers.api_get(f'{BASE_URL}recipes/{recipe_id}') or {}
    context = {
        'recipe': recipe,
        'input_field': recipe_data_user_input
    }
    template = 'App/edit_recipe.html'
    return render(request, template, context)


def delete_recipe(request, recipe_id):
    if request.method == 'POST':
        if not helpers.api_delete(f'{BASE_URL}recipes/{recipe_id}'):
            messages.error(request, 'Failed to delete the recipe, please try again.')

    context = {
        'recipe_id': recipe_id,
        'messages': messages.get_messages(request)
    }
    template = 'App/delete_recipe.html'
    return render(request, template, context)
