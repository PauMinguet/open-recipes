# generated by fastapi-codegen:
#   filename:  openapi.yaml
#   timestamp: 2023-10-24T00:41:23+00:00

from __future__ import annotations

from typing import List, Union

from fastapi import FastAPI, Form, Query, Request
from typing import Annotated, Optional
from sqlalchemy.engine import Engine
from fastapi import Depends
from open_recipes.models import Ingredient, Recipe, RecipeList, Review, User, PopulatedRecipe, CreateUserRequest, CreateRecipeListRequest, CreateRecipeRequest, RecipeListResponse, Tag, CreateTagRequest
from open_recipes.database import get_engine 
from sqlalchemy import text, func, distinct, case
import sqlalchemy
import uvicorn
from pydantic import BaseModel
from open_recipes.api.users import router as user_router
from open_recipes.api.recipes import router as recipe_router 
from open_recipes.api.ingredients import router as ingredient_router
from open_recipes.api.tags import router as tag_router 



app = FastAPI(
    title='Recipe Service API',
    version='1.0.0',
    description='API for managing recipes, ingredients, users, and reviews.',
)

app.include_router(user_router)
app.include_router(recipe_router)
app.include_router(ingredient_router)
app.include_router(tag_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}

#SMOKE TESTED
@app.get('/recipe-lists', response_model=List[RecipeList])
def get_recipe_lists(engine : Annotated[Engine, Depends(get_engine)]) -> List[RecipeList]:
    """
    Get all recipe lists
    """
    recipeListAll = []
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT id, name, description FROM recipe_list ORDER BY id"))
        rows = result.fetchall()
        for row in rows: 
            id, name, description = row
            recipe = RecipeList(id=id, name=name, description=description)
            recipeListAll.append(recipe)
        return recipeListAll
@app.post(
    '/recipe-lists', response_model=None, status_code=201, responses={'201': {'model': RecipeList}}
)
def post_recipe_lists(body: CreateRecipeListRequest,engine : Annotated[Engine, Depends(get_engine)]) -> Union[None, RecipeList]:
    """
    Create a new recipe list
    """
    with engine.begin() as conn:
        result = conn.execute(text(f"""INSERT INTO recipe_list (name, description)
                                    VALUES (:name, :description)
                                    RETURNING id, name, description 
                                   """
                                    ),{"name":body.name,"description":body.description})
        
        id, name, description= result.fetchone()
        #print(id, name, description)
        return RecipeList(id=id, name=name, description=description)

@app.post('/recipe-lists/{recipe_list_id}/recipe/{recipe_id}',status_code=201, response_model=Recipe)
def post_recipe_to_list(recipe_id: int, recipe_list_id: int,engine : Annotated[Engine, Depends(get_engine)]) -> Recipe:
    """
    Add a recipe to a recipe list
    """
    with engine.begin() as conn:
        result = conn.execute(text(f"""INSERT INTO recipe_x_recipe_list (recipe_id, recipe_list_id)
                                    VALUES (:recipe_id, :recipe_list_id)
                                    RETURNING recipe_id, recipe_list_id 
                                   """
                                    ),{"recipe_id":recipe_id,"recipe_list_id":recipe_list_id})
        
        recipe_id, recipe_list_id = result.fetchone()
        return Recipe(recipe_id=recipe_id, recipe_list_id=recipe_list_id)

#SMOKE TESTED
@app.get('/recipe-lists/{id}', response_model=RecipeListResponse)
def get_recipe_list(id: int,engine : Annotated[Engine, Depends(get_engine)]) -> RecipeList:
    """
    Get a recipe list by id
    """
    with engine.begin() as conn:
        result = conn.execute(text(f"""SELECT id, name, description FROM recipe_list WHERE id = :recipe_id"""),{"recipe_id": id})
        id, name, description = result.fetchone()
        result = conn.execute(text(f"""SELECT id, name, description, mins_prep, mins_cook, default_servings, author_id, procedure
                                        FROM recipe
                                        JOIN recipe_x_recipe_list AS rl ON rl.recipe_id = recipe.id
                                        WHERE rl.recipe_list_id = :list_id"""),{"list_id": id})
        rows = result.fetchall()
        recipes = [Recipe(id=row.id, name=row.name, description=row.description, mins_prep=row.mins_prep, mins_cook=row.mins_cook, default_servings=row.default_servings, author_id=row.author_id, procedure=row.procedure) for row in rows]
        #print(recipes)
        return RecipeListResponse(id=id, name=name, description= description, recipes=recipes)

# @app.post("/recipe-lists/{id}")
# def update_recipe_list(id: int, recipe_list : RecipeList, engine : Annotated[Engine, Depends(get_engine)]) -> RecipeList:
#     with engine.begin() as conn:
#         result = conn.execute(text(f"""UPDATE recipe_list 
#                                    SET name = :name, description = :description
#                                    WHERE id = :id""",{"name":recipe_list.name, "description":recipe_list.description, "id":id}))
#         id, name, description = result.fetchone()
#         return RecipeList(id=id, name=name, description=description)

# @app.delete("/recipe-lists/{id}")
# def delete_recipe_list(id: int,engine : Annotated[Engine, Depends(get_engine)]) -> None:
#     with engine.begin() as conn:
#         result = conn.execute(text(f"""DELETE FROM recipe_list 
#                                    WHER
#                                    default_servings, procedure FROM "recipe" """))
#         id, name, mins_prep, category_id, mins_cook, description, author_id, default_servings, procedure = result.fetchone()
#         return Recipe(id=id, name=name, mins_prep=mins_prep, category_id=category_id, mins_cook=mins_cook, description=description, author_id=author_id, default_servings=default_servings, procedure=procedure)
 


class SearchResults(BaseModel):
    recipe: List[Recipe]
    next_cursor: Optional[int]
    prev_cursor: Optional[int]
    
# @app.get('/reviews', response_model=List[Review])
# def get_reviews(engine : Annotated[Engine, Depends(get_engine)]) -> List[Review]:
#     """
#     Get all reviews
#     """
#     with engine.begin() as conn:
#         result = conn.execute(text(f"SELECT id, stars, author_id, content, recipe_id, FROM reviews ORDER BY created_at"))
#         id, name, email, phone = result.fetchone()
#         return User(id=id, name=name, email=email, phone=phone)

# @app.post('/reviews', response_model=None, responses={'201': {'model': Review}})
# def post_reviews(body: Review,engine : Annotated[Engine, Depends(get_engine)]) -> Union[None, Review]:
#     """
#     Create a new review
#     """
#     with engine.begin() as conn:
#         result = conn.execute(text(f"INSERT INTO reviews stars, author_id, content, recipe_id values (:stars,:author_id,:content,:recipe_id)",{"stars":body.stars,"author_id":body.author.id,"content":body.content,"recipe_id":body.recepie.id}))
#         id, stars, author_id, content, recipe_id = result.fetchone()
#         return User(id=id, stars=stars, author_id=author_id, content=content, recipe_id = recipe_id)

# @app.get('/reviews/{id}', response_model=Review)
# def get_review(id: int,engine : Annotated[Engine, Depends(get_engine)]) -> Review:
#     """
#     Get a review by id
#     """
#     with engine.begin() as conn:
#         result = conn.execute(text(f"""SELECT stars, author_id, content, recipe_id FROM review WHERE id = :id"""),{"id":id})
#         id, stars, author_id, content, recipe_id = result.fetchone()
#         return Review(id=id, stars=stars, author_id=author_id, content=content, recipe_id = recipe_id)

# @app.post("/reviews/{id}")
# def update_review(id: int, review : Review,engine : Annotated[Engine, Depends(get_engine)]) -> Review:
#     with engine.begin() as conn:
#         result = conn.execute(text(f"UPDATE review SET stars = :stars, author_id = :author_id, content = :content, recipe_id = :recipe_id WHERE id = :id",{"stars":review.stars,"author_id":review.author_id, "content":review.content,  "recipe_id":review.recipe_id, "id":id}))
#         id, stars, author_id, content, recipe_id = result.fetchone()
#         return Review(id=id, stars = stars, author_id = author_id, content = content, recipe_id = recipe_id)

# @app.delete("/reviews/{id}")
# def delete_review(id: int,engine : Annotated[Engine, Depends(get_engine)]) -> None:
#     with engine.begin() as conn:
#         result = conn.execute(text(f"""DELETE FROM "reviews" WHERE id = :id""",{"id":id}))
#         id, stars, author_id, content, recipe_id = result.fetchone()
#         return Review(id=id, stars=stars, author_id=author_id, content=content, recipe_id = recipe_id)


@app.post('/test-post')
async def test_post(request: Request):
    # Access query parameters from the URL
    query_params = dict(request.query_params)

    # Access data from the request body (assuming it's JSON)
    try:
        data = await request.json()
    except ValueError:
        data = None  # Set data to None if no JSON data is sent

    # Prepare the response data
    response_data = {
        'request_data': data,
        'query_parameters': query_params,
    }

    return response_data



if __name__ == "__main__":
    import uvicorn

    config = uvicorn.Config(
        app, port=3000, log_level="info", reload=True
    )
    server = uvicorn.Server(config)
    server.run()
