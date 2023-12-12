import requests  # library used to handle HTTP requests
import json  # helps with json processing
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def api_get(url):
    """
    Send a GET request to the specified URL.

    Args:
    url (str): The URL to which the GET request is sent.

    Returns:
    dict or None: The JSON response parsed into a dictionary if the response status is 200; otherwise, None.
    """
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        logger.error(f"Error during GET request to {url}: {e}")
        return None


def api_post(url, data):
    """
    Send a POST request to the specified URL with the provided data.

    Args:
    url (str): The URL to which the POST request is sent.
    data (dict): The data to be sent in the POST request.

    Returns:
    bool: True if the response status code is 200, indicating success; False otherwise.
    """
    try:
        response = requests.post(url, json=data)
        return response.status_code == 200
    except requests.RequestException as e:
        logger.error(f"Error during POST request to {url}: {e}")
        return False


def api_put(url, data):
    """
    Send a PUT request to the specified URL with the provided data.

    Args:
    url (str): The URL to which the PUT request is sent.
    data (dict): The data to be sent in the PUT request.

    Returns:
    bool: True if the response status code is 200, indicating success; False otherwise.
    """
    try:
        response = requests.put(url, json=data)
        return response.status_code == 200
    except requests.RequestException as e:
        logger.error(f"Error during PUT request to {url}: {e}")
        return False


def api_delete(url):
    """
    Send a DELETE request to the specified URL.

    Args:
    url (str): The URL to which the DELETE request is sent.

    Returns:
    bool: True if the response status code is 200, indicating successful deletion; False otherwise.
    """
    try:
        response = requests.delete(url)
        return response.status_code == 200
    except requests.RequestException as e:
        logger.error(f"Error during DELETE request to {url}: {e}")
        return False


def recipe_data_to_json(recipe_data_user_input):
    """
    Convert the recipe data from user input (a string) into JSON format.

    Args:
    recipe_data_user_input (str): A string containing the recipe data.

    Returns:
    dict: The recipe data in JSON (dictionary) format, or None if an error occurs.
    """
    try:
        # Split the input into lines
        lines = recipe_data_user_input.split('\n')

        # Assuming components would be provided in this format
        title = lines[0]
        serving_size = int(lines[1])  # Convert serving size to an integer
        ingredients = lines[2]
        steps = lines[3:]

        # Construct the recipe JSON (dictionary)
        recipe_json = {
            'title': title,
            'serving_size': serving_size,
            'ingredients': ingredients,
            'instructions': steps
        }

        return recipe_json

    except Exception as e:
        # Log the exception and return None or handle it as needed
        logger.error(f"Error processing recipe data: {e}")
        return None
