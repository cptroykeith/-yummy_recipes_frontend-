"""
This includes the tests for the User Object
"""

import unittest
from app.models import Database, User, Recipe, RecipeCategory, \
RecipeStep
from app import utilities

class DatabaseTest(unittest.TestCase):
    """
    Tests for the Database class
    """

    def setUp(self):
        """Declares variables to be used in most tests"""
        self.db = Database()
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'password',
            }
        self.user = User(**self.user_data, key=1)
        self.category_data = {
            'key': 1,
            'name': 'cakes',
            'description': 'all recipes cake!',
            'user': self.user.key,
        }
        self.recipe_data = {
            'key': 1,
            'name': 'breadcake',
            'description': 'yummy',
            'category': self.category_data['key'],
        }
        self.recipe_step_data = {
            'key': 1,
            'text_content': "Don't do anything",
            'recipe': self.recipe_data['key'],
        }

    def test_get_next_key(self):
        """The next key for each model object type can be got"""
        self.assertEqual(self.db.get_next_key(User), 1)
        self.assertEqual(self.db.get_next_key(Recipe), 1)
        self.assertEqual(self.db.get_next_key(RecipeCategory), 1)
        self.assertEqual(self.db.get_next_key(RecipeStep), 1)
        self.db._user_keys += [1,2,3]
        self.assertEqual(self.db.get_next_key(User), 4)
        self.db._recipe_keys += [1,2,3,7]
        self.assertEqual(self.db.get_next_key(Recipe), 8)
        self.db._recipe_category_keys += [1,2,3, 4]
        self.assertEqual(self.db.get_next_key(RecipeCategory), 5)
        self.db._recipe_step_keys += [1,2,3,9]
        self.assertEqual(self.db.get_next_key(RecipeStep), 10)
        self.assertRaises(TypeError, self.db.get_next_key, 2)

    def test_create_user(self):
        """A user can be created in 'Database'"""
        user = self.db.create_user(self.user_data)
        self.assertIsInstance(user, User)
        self.assertIn(user.key, self.db.user_keys)
        self.assertEqual(user, self.db.users[user.key])
        self.assertIn(user.email, self.db.user_email_key_map.keys())
        self.assertEqual(user.key, self.db.user_email_key_map[user.email])

    def test_get_user(self):
        """A user can be got by user_key"""
        user = User(**self.user_data, key=1)
        user.save(self.db)
        user_from_db = self.db.get_user(user.key)
        self.assertEqual(user, user_from_db)
        non_existent_key = 3
        self.assertIsNone(self.db.get_user(non_existent_key))
        self.assertRaises(TypeError, self.db.get_user, 'user_key should be int')

    def test_get_user_by_email(self):
        """A user can be got by email"""
        user = self.db.create_user(self.user_data)
        self.assertIsInstance(user, User)
        user_instance = self.db.get_user_by_email(user.email)
        self.assertEqual(user, user_instance)
        self.assertRaises(TypeError, self.db.get_user_by_email, 2)

    def test_get_recipe_category(self):
        """A recipe category can be retrieved by key"""
        # setup
        self.user.save(self.db)
        # create category
        category = RecipeCategory(**self.category_data)
        # save category
        category.save(self.db)
        # try retrieving the category
        category_from_db = self.db.get_recipe_category(category.key)
        self.assertEqual(category, category_from_db)
        # try retrieving a non-existent category
        self.assertIsNone(self.db.get_recipe_category(4))
        # try using a non-int key
        self.assertRaises(TypeError, self.db.get_recipe_category, 'string instead of int')

    def test_delete_object_for_category(self):
        """delete_object should be able to remove the object passed to it from the database"""
        # setup
        self.user.save(self.db)
        # create category
        category = RecipeCategory(**self.category_data)
        # save category
        category.save(self.db)
        # create recipe
        recipe = Recipe(**self.recipe_data)
        # save recipe as child of category due to key set in setUp
        recipe.save(self.db)
        # delete category
        ##################Test deleting categories####################
        self.db.delete_object(category)
        # assert that the category object is not in self.db.recipe_categories
        self.assertRaises(KeyError, utilities.return_value_from_dict, self.db.recipe_categories, category.key)
        # assert that the recipe object is not in self.db.recipes
        self.assertRaises(KeyError, utilities.return_value_from_dict, self.db.recipes, recipe.key)
        # assert that the category key is not in self.db.recipe_category_keys
        self.assertNotIn(category.key, self.db.recipe_category_keys)
        # assert that the recipe key is not in self.db.recipe_keys
        self.assertNotIn(recipe.key, self.db.recipe_keys)
        # assert that the category name is not in self.db.recipe_categories_name_key_map
        self.assertNotIn(category.name, self.db.recipe_category_name_key_map.keys())
        # assert that the recipe name is not in self.db.recipe_name_key_map
        self.assertNotIn(recipe.name, self.db.recipe_name_key_map.keys())
        # try to delete a non existent object by deleting category again
        self.assertRaises(KeyError, self.db.delete_object, category)
        # try to delete an object of a type that does not exist in database
        self.assertRaises(TypeError, self.db.delete_object, 2)

    def test_delete_object_for_recipes(self):
        """delete_object should be able to remove the object passed to it from the database"""
        # setup
        self.user.save(self.db)
        category = RecipeCategory(**self.category_data)
        category.save(self.db)
        recipe = Recipe(**self.recipe_data)
        recipe.save(self.db)
        # create step as child of recipe
        recipe_step = RecipeStep(**self.recipe_step_data)
        recipe_step.save(self.db)
        # delete recipe
        self.db.delete_object(recipe)
        # assert that the recipe step object is not in self.db.recipe_steps
        self.assertRaises(KeyError, utilities.return_value_from_dict, self.db.recipe_steps, recipe_step.key)
        # assert that the recipe object is not in self.db.recipes
        self.assertRaises(KeyError, utilities.return_value_from_dict, self.db.recipes, recipe.key)
        # assert that the recipe step key is not in self.db.recipe_step_keys
        self.assertNotIn(recipe_step.key, self.db.recipe_step_keys)
        # assert that the recipe key is not in self.db.recipe_keys
        self.assertNotIn(recipe.key, self.db.recipe_keys)
        # assert that the recipe name is not in self.db.recipe_name_key_map
        self.assertNotIn(recipe.name, self.db.recipe_name_key_map.keys())
        # try to delete a non existent object by deleting category again
        self.assertRaises(KeyError, self.db.delete_object, recipe)

    def test_get_recipe(self):
        """A recipe can be retrieved by key"""
        # setup
        self.user.save(self.db)
        category = RecipeCategory(**self.category_data)
        category.save(self.db)
        recipe = Recipe(**self.recipe_data)
        recipe.save(self.db)
        # try retrieving the recipe
        recipe_from_db = self.db.get_recipe(recipe.key)
        self.assertEqual(recipe, recipe_from_db)
        # try retrieving a non-existent recipe
        self.assertIsNone(self.db.get_recipe(4))
        # try using a non-int key
        self.assertRaises(TypeError, self.db.get_recipe, 'string instead of int')

    def test_get_recipe_step(self):
        """A recipe step can be retrieved by key"""
        # setup
        self.user.save(self.db)
        category = RecipeCategory(**self.category_data)
        category.save(self.db)
        recipe = Recipe(**self.recipe_data)
        recipe.save(self.db)
        recipe_step = RecipeStep(**self.recipe_step_data)
        recipe_step.save(self.db)
        # try retrieving the recipe step
        recipe_step_from_db = self.db.get_recipe_step(recipe_step.key)
        self.assertEqual(recipe_step, recipe_step_from_db)
        # try retrieving a non-existent recipe step
        self.assertIsNone(self.db.get_recipe_step(50))
        # try using a non-int key
        self.assertRaises(TypeError, self.db.get_recipe_step, 'string instead of int')


        



    # key should not be negative or zero
    # key should not exist already


if __name__ == '__main__':
    unittest.main()
    