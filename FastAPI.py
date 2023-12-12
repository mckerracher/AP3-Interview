from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Ingredient(BaseModel):
    item: str
    quantity: float  # Numerical quantity
    unit: Optional[str] = None  # Optional unit of measurement
    description: Optional[str] = None  # Optional additional description


class Recipe(BaseModel):
    title: str
    instructions: List[str]  # List of instruction steps
    ingredients: List[Ingredient]
    serving_size: int  # Number of servings


recipes_database_placeholder = {}  # let's assume this is the PostgreSQL DB


@app.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: int, recipe: Recipe):
    """
    Update an existing recipe.

    Args:
    recipe_id (int): The ID of the recipe to update.
    recipe (Recipe): The updated recipe data.

    Returns:
    dict: A success message.
    """
    try:
        if recipe_id not in recipes_database_placeholder:
            logger.warning(f"Recipe with ID {recipe_id} not found")
            raise HTTPException(status_code=404, detail="Recipe not found")
        recipes_database_placeholder[recipe_id] = recipe  # update existing recipe with the new version
        logger.info(f"Recipe with ID {recipe_id} updated successfully")
        return {"message": "Recipe updated successfully"}
    except Exception as e:
        logger.error(f"Error updating recipe with ID {recipe_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating recipe")
