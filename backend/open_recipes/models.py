# generated by fastapi-codegen:
#   filename:  openapi.yaml
#   timestamp: 2023-10-24T00:41:23+00:00

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


# TODO: define all request types
class CreateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class User(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class AuthorResponseUser(BaseModel):
    id: int
    name: str


class SignUpRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class RecepieTag(BaseModel):
    id: Optional[int] = None
    key: Optional[str] = None
    value: Optional[str] = None


class CreateRecipeRequest(BaseModel):
    name: Optional[str] = None
    mins_prep: Optional[int] = None
    mins_cook: Optional[int] = None
    description: Optional[str] = None
    default_servings: Optional[int] = None
    procedure: Optional[str] = None
    created_at: Optional[str] = None
    calories: Optional[int] = None
    tags: Optional[List[Any]] = []  # List of CreateTagRequest
    ingredients: Optional[List[Any]] = []  # List of CreateIngredientRequest


class Recipe(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    mins_prep: Optional[int] = None
    mins_cook: Optional[int] = None
    description: Optional[str] = None
    default_servings: Optional[int] = None
    created_at: Optional[str] = None
    author_id: Optional[str] = None
    procedure: Optional[str] = None
    calories: Optional[int] = None


class PopulatedRecipe(Recipe):
    author: AuthorResponseUser = None
    tags: list[RecepieTag] = []
    ingredients: list[IngredientWithAmount] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = kwargs.get("author", None)
        self.tags = kwargs.get("tags", [])


class CreateRecipeListRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class RecipeListResponse(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    recipes: list[Recipe] = []


class RecipeList(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None

    def get_recipes(self, engine):
        with engine.connect() as conn:
            result = conn.execute(
                """
                SELECT id, name, mins_prep, category_id, mins_cook, description, author_id, default_servings
                FROM recipe
                JOIN recipe_x_recipe_list as rxl ON recipe.id = rxl.recipe_id
                WHERE recipe_list_id = :my_id
                """,
                {"my_id": self.id},
            )
            rows = result.fetchall()
            return [
                Recipe(
                    id=row[0],
                    name=row[1],
                    mins_prep=row[2],
                    category_id=row[3],
                    mins_cook=row[4],
                    description=row[5],
                    author_id=row[6],
                    default_servings=row[7],
                )
                for row in rows
            ]

    def create_populated(self) -> PopulatedRecipeList:
        recipes = self.get_recipes()  # Fetch all recipes
        return PopulatedRecipeList(
            id=self.id, name=self.name, description=self.description, recipes=recipes
        )


class PopulatedRecipeList(RecipeList):
    recipes: list[Recipe] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recipes = kwargs.get("recipes", [])


class Review(BaseModel):
    id: Optional[int] = None
    stars: Optional[int] = None
    author: Optional[User] = None
    content: Optional[str] = None
    recepie: Optional[Recipe] = None
    created_at: Optional[str] = None


class BareReview(BaseModel):
    id: Optional[int] = None
    stars: Optional[int] = None
    author_id: Optional[str] = None
    content: Optional[str] = None
    recepie_id: Optional[str] = None
    created_at: Optional[str] = None

    def to_review(self, engine):
        with engine.connect() as conn:
            user = User.get_by_id(conn, self.author_id)
            recepie_result = conn.execute(
                f"""
                SELECT * FROM recepies WHERE id = {self.recepie_id}
                """
            )
            recepie = Recipe(recepie_result.first())
            return Review(
                id=self.id,
                stars=self.stars,
                author=user,
                content=self.content,
                recepie=recepie,
                created_at=self.created_at,
            )


class IngredientCategory(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None


class Ingredient(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    category_id: Optional[int] = None
    type: Optional[str] = None
    storage: Optional[str] = None
    # storage: Optional[Literal["FRIDGE"] | Literal["FREEZER"] | Literal["PANTRY"]] = None


class CreateIngredientRequest(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    type: Optional[str] = None
    storage: Optional[str] = None

    # storage: Optional[Literal["FRIDGE"] | Literal["FREEZER"] | Literal["PANTRY"]] = None


class CreateIngredientWithAmount(CreateIngredientRequest):
    quantity: Optional[int] = None
    unit: Optional[str] = None


class IngredientWithAmount(Ingredient):
    quantity: Optional[int] = None
    unit: Optional[str] = None


class Tag(BaseModel):
    id: Optional[int] = None
    key: Optional[str] = None
    value: Optional[str] = None


class CreateTagRequest(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None


PopulatedRecipe.update_forward_refs()
