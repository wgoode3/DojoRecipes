# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..user_app.models import User

class RecipeManager(models.Manager):
    def addRecipe(self, recipeData, user):
        errors = []

        if len(recipeData["name"]) < 1:
            errors.append("Recipe name is required")
        elif len(recipeData["name"]) < 3:
            errors.append("Recipe name must be 3 characters or more")

        if(len(recipeData["ingredients"]) < 1):
            errors.append("Ingredients are required for a recipe")
        else:
            ingredients = recipeData["ingredients"].split(",")
            valid = True
            if len(ingredients) < 3:
                valid = False
            for ingredient in ingredients:
                if len(ingredient.split(" ")) < 3:
                    valid = False

            if not valid:
                errors.append("Invalid list of ingredients, you must have at least 3 ingredients with each ingredient seperated by spaces with name and amount and units")

        if len(recipeData["instructions"]) < 1:
            errors.append("Instructions are required for a recipe")
        elif len(recipeData["instructions"]) < 10:
            errors.append("Instructions must be 10 characters or more")

        if len(errors) > 0:
            return (False, errors)

        list_of_ingredients = []

        for ingredient in ingredients:
            i = ingredient.split(" ")
            list_of_ingredients.append([" ".join(i[:-2]).lstrip(' '), i[-2], i[-1]])

        for i in range(len(list_of_ingredients)):
            list_of_ingredients[i].append(Ingredient.objects.addIngredient(list_of_ingredients[i][0]))

        recipe = Recipe.objects.create(
            name = recipeData["name"],
            instructions = recipeData["instructions"],
            creator_id = user
        )

        for i in range(len(list_of_ingredients)):
            Amount.objects.create(
                amount = list_of_ingredients[i][1],
                units = list_of_ingredients[i][2],
                ingredient_id = list_of_ingredients[i][3],
                recipe_id = recipe.id
            )

        return (True)

class IngredientManager(models.Manager):
    def addIngredient(self, name):
        list_of_ingredients = Ingredient.objects.filter(name=name)
        if len(list_of_ingredients) > 0:
            return list_of_ingredients[0].id
        else:
            ingredient = Ingredient.objects.create(name=name)
            return ingredient.id

class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    objects = IngredientManager()

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    instructions = models.TextField(max_length=2000)
    creator = models.ForeignKey(User, related_name="my_recipes")
    likes = models.ManyToManyField(User, related_name="liked_recipes")

    objects = RecipeManager()

class Amount(models.Model):
    amount = models.CharField(max_length=255)
    units = models.CharField(max_length=255)
    ingredient = models.ForeignKey(Ingredient, related_name="recipes_used")
    recipe = models.ForeignKey(Recipe, related_name="ingredients")
