# generated by fastapi-codegen:
#   filename:  openapi.yaml
#   timestamp: 2023-10-24T00:41:23+00:00

from __future__ import annotations

from typing import List, Union

from fastapi import FastAPI

from open_recipes.models import Ingredient, Recipe, RecipeList, Review, User, PopulatedRecipe, CreateUserRequest, CreateRecipeListRequest, CreateRecipeRequest, RecipeListResponse
from open_recipes.database import engine 
from sqlalchemy import text
import uvicorn

app = FastAPI(
    title='Recipe Service API',
    version='1.0.0',
    description='API for managing recipes, ingredients, users, and reviews.',
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/ingredients', response_model=List[Ingredient])
def get_ingredients() -> List[Ingredient]:
    """
    Get all ingredients
    """
    pass

@app.get('/ingredients/{id}', response_model=Ingredient)
def get_ingredient(id : int) -> Ingredient:
    """
    Get an ingredient by id
    """
    pass

@app.post("/ingredients/{id}")
def update_ingredient(id: int, ingredient : Ingredient) -> Ingredient:
    with engine.begin() as conn:
        result = conn.execute(text(f"UPDATE ingredients SET name = :name, email = :email, phone = :phone WHERE id = :id",{"name":ingredient.name,"email":ingredient.email,"phone":ingredient.phone,"id":id}))
        id, name, email, phone = result.fetchone()
        return User(id=id, name=name, email=email, phone=phone) 

@app.delete("/ingredient/{id}")
def delete_ingredient(id: int) -> None:
    pass

@app.post('/ingredients', response_model=None, responses={'201': {'model': Ingredient}})
def post_ingredients(body: Ingredient) -> Union[None, Ingredient]:
    """
    Create a new ingredient
    """
    pass

#SMOKE TESTED
@app.get('/recipe-lists', response_model=List[RecipeList])
def get_recipe_lists() -> List[RecipeList]:
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
    pass

#SMOKE TESTED
@app.post(
    '/recipe-lists', response_model=None, status_code=201, responses={'201': {'model': RecipeList}}
)
def post_recipe_lists(body: CreateRecipeListRequest) -> Union[None, RecipeList]:
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
        return RecipeList(id=id, name=name, description=description)

#SMOKE TESTED
@app.get('/recipe-lists/{id}', response_model=None)
def get_recipe_list(id: int) -> RecipeList:
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
        recipes = [Recipe(id=row[0], name=row[1], mins_prep=row[2], mins_cook=row[3], description=row[4], default_servings=row[5], author_id=row[6], procedure=row[7]) for row in rows]
        return RecipeListResponse(id=id, name=name, description= description, recipes=recipes)

@app.post("/recipe-lists/{id}")
def update_recipe_list(id: int, recipe_list : RecipeList) -> RecipeList:
    pass

@app.delete("/recipe-lists/{id}")
def delete_recipe_list(id: int) -> None:
    pass

#TODO: fixme and implement search
@app.get('/recipes', response_model=List[Recipe])
def get_recipes() -> List[Recipe]:
    """
    Get all recipes
    """
    with engine.begin() as conn:
        result = conn.execute(text(f"""SELECT id, name, email, phone FROM "user" """))
        id, name, email, phone = result.fetchone()
        return User(id=id, name=name, email=email, phone=phone)
    

#SMOKE TESTED
#FIXME: increment created at in database
@app.post('/recipes', response_model=None, status_code=201, responses={'201': {'model': CreateRecipeRequest}})
def post_recipes(body: CreateRecipeRequest) -> Union[None, Recipe]:
    """
    Create a new recipe
    """    
    with engine.begin() as conn:
        result = conn.execute(text(f"""INSERT INTO recipe (name, mins_prep, mins_cook, description, default_servings, author_id, procedure)
                                   VALUES (
                                   :name,
                                   :mins_prep,
                                   :mins_cook,
                                   :description,
                                   :default_servings,
                                   :author_id,
                                   :procedure)
                                   RETURNING id, name, mins_prep, mins_cook, description, default_servings, author_id, procedure"""
                                   
            ), {"name":body.name,
             "author_id":body.author_id,
             "mins_prep":body.mins_prep,
             "mins_cook":body.mins_cook
             ,"description":body.description,
             "default_servings":body.default_servings,
             "procedure":body.procedure})
        id,name,mins_prep,mins_cook,description,default_servings,author_id,procedure = result.fetchone()
        recipe = Recipe(id=id,name=name,mins_prep=mins_prep,mins_cook=mins_cook,description=description,default_servings=default_servings,author_id=author_id, procedure=procedure)
        return recipe

#SMOKE TESTED
@app.get('/recipes/{id}', response_model=Recipe)
def get_recipe(id: int) -> Recipe:
    """
    Get a recipe by id
    """
    with engine.begin() as conn:
        result = conn.execute(text(f"""SELECT id, name, mins_prep, mins_cook, description, default_servings, author_id, procedure FROM recipe WHERE id = :id"""),{"id":id})
        id, name, mins_prep,mins_cook,description,default_servings,author_id,procedure = result.fetchone()
        return Recipe(id=id,name=name,mins_prep=mins_prep,mins_cook=mins_cook,description=description,default_servings=default_servings,author_id=author_id, procedure=procedure)

@app.post("/recipes/{id}", status_code=201, response_model=None)
def update_recipe(id: int, recipe : Recipe) -> Recipe:
    pass

@app.delete("/recipes/{id}")
def delete_recipe(id: int) -> None:
    pass

@app.post('/recipes/{recipe_id}/recipe-lists/{recipe_list_id}', status_code=201, response_model=None)
def add_recipe_to_recipe_list(recipe_id: int, recipe_list_id: int) -> None:
    with engine.begin() as conn:
        conn.execute(text(f"INSERT INTO recipe_x_recipe_list (recipe_id, recipe_list_id) VALUES (:recipe_id, :recipe_list_id)"),{"recipe_id":recipe_id,"recipe_list_id":recipe_list_id})
        return "OK"

@app.get('/reviews', response_model=List[Review])
def get_reviews() -> List[Review]:
    """
    Get all reviews
    """
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT id, stars, author_id, content, recipe_id, FROM reviews ORDER BY created_at"))
        id, name, email, phone = result.fetchone()
        return User(id=id, name=name, email=email, phone=phone)

@app.post('/reviews', response_model=None, responses={'201': {'model': Review}})
def post_reviews(body: Review) -> Union[None, Review]:
    """
    Create a new review
    """
    with engine.begin() as conn:
        result = conn.execute(text(f"INSERT INTO reviews stars, author_id, content, recipe_id values (:stars,:author_id,:content,:recipe_id)",{"stars":body.stars,"author_id":body.author.id,"content":body.content,"recipe_id":body.recepie.id}))
        id, name, email, phone = result.fetchone()
        return User(id=id, name=name, email=email, phone=phone)

@app.get('/reviews/{id}', response_model=Review)
def get_review(id: int) -> Review:
    """
    Get a review by id
    """
    pass

@app.post("/reviews/{id}")
def update_review(id: int, review : Review) -> Review:
    pass

@app.delete("/reviews/{id}")
def delete_review(id: int) -> None:
    pass

@app.get('/users', response_model=List[User])
def get_users() -> List[User]:
    """
    Get all users
    """
    with engine.begin() as conn:
        result = conn.execute(text(f"SELECT id, name, email, phone FROM "user" ORDER BY id"))
        id, name, email, phone = result.fetchone()
        return User(id=id, name=name, email=email, phone=phone)

#SMOKE TESTED
@app.get('/users/{user_id}',response_model=User)
def get_user(user_id: int) -> List[User]:
    """
    Get one user
    """
    with engine.begin() as conn:
        result = conn.execute(text(f"""SELECT id, name, email, phone FROM "user" WHERE id = :user_id"""),{"user_id":user_id})
        id, name, email, phone = result.fetchone()
        return User(id=id, name=name, email=email, phone=phone)

#SMOKE TESTED
@app.post('/users', response_model=None,status_code=201, responses={'201': {'model': User}})
def post_users(body: CreateUserRequest) -> Union[None, User]:
    """
    Create a new user
    """
    with engine.begin() as conn:
        result = conn.execute(text(f"""INSERT INTO "user" (name, email, phone)
                                    VALUES (:name, :email, :phone)
                                    RETURNING id, name, email, phone
                                   """
                                    ),{"name":body.name,"phone":body.phone,"email":body.email})
        
        id, name, email, phone = result.fetchone()
        return User(id=id, name=name, email=email, phone=phone)

@app.post("/users/{id}")
def update_user(id: int, user : User) -> User:

    with engine.begin() as conn:
        result = conn.execute(text(f"UPDATE users SET name = :name, email = :email, phone = :phone WHERE id = :id",{"name":user.name,"phone":user.phone,"email":user.email,"id":id}))
        id, name, email, phone = result.fetchone()
        return User(id=id, name=name, email=email, phone=phone)

@app.delete("/users/{id}")
def delete_user(id: int) -> None:
    with engine.begin() as conn:
        result = conn.execute(text(f"""DELETE FROM "user" WHERE id = :id""",{"id":id}))
        id, name, email, phone = result.fetchone()
        return User(id=id, name=name, email=email, phone=phone)



import uvicorn

if __name__ == "__main__":
    config = uvicorn.Config(
        app, port=3000, log_level="info", reload=True
    )
    server = uvicorn.Server(config)
    server.run()
