"""Module containing all the tests for Recipe class"""


import unittest
from app.models import Database, User, RecipeCategory,\
Recipe, RecipeStep
from app import utilities


class RecipeTest(unittest.TestCase):
    """All tests for the Recipe class"""
    
    def setUp(self):
        """Initiates variables to be used in most tests"""
        self.db = Database()
        self.user_data = {
            'key': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'password',
            }
        self.user = User(**self.user_data)
        self.db = Database()
        self.user.save(self.db)
        self.category_data = {
            'key': 1,
            'name': 'cakes',
            'description': 'all recipes cake!',
            'user': self.user.key,
        }
        self.category = RecipeCategory(**self.category_data)
        self.category.save(self.db)
        self.recipe_data = {
            'key': 1,
            'name': 'Banana cake',
            'description': 'yummy!',
            'category': self.category.key
        }
        self.recipe = Recipe(**self.recipe_data)
        self.recipe_step_data = {
            'text_content': "Don't do anything",
        }

    def test_name_is_mandatory(self):
        """
        In the constructor, the name parameter should be 
        a string which is not empty
        """
        self.assertRaises(TypeError, Recipe, key=1,
                          description='', category=self.category.key)
        invalid_data = utilities.replace_value_in_dict(self.recipe_data, 'name', 7)
        self.assertRaises(TypeError, Recipe, **invalid_data)
        invalid_data = utilities.replace_value_in_dict(self.recipe_data, 'name', '')
        self.assertRaises(ValueError, Recipe, **invalid_data)
        invalid_data = utilities.replace_value_in_dict(self.recipe_data, 'name', ' ')
        self.assertRaises(ValueError, Recipe, **invalid_data)

    def test_save_method(self):
        """
        The save() method should be able to update the parent category's 
        list of recipes as well as that of the database
        """
        self.assertIsInstance(self.recipe, Recipe)
        self.recipe.save(self.db)
        length_of_db_recipe_keys = len(self.db.recipe_keys)
        length_of_category_recipes = len(self.category.recipes)
        self.assertIn(self.recipe.key, self.db.recipe_keys)
        self.assertEqual(self.recipe, self.db.recipes[self.recipe.key])
        self.assertIn(self.recipe.key, self.category.recipes)
        self.assertIn(self.recipe.name, self.db.recipe_name_key_map.keys())
        self.assertEqual(self.recipe.key,
                         self.db.recipe_name_key_map[self.recipe.name])
        # the category should exist in database
        invalid_data = utilities.replace_value_in_dict(self.recipe_data, 'category', 78)
        new_recipe = Recipe(**invalid_data)
        self.assertRaises(KeyError, new_recipe.save, self.db)
        # database parameter should be of type Database
        self.assertRaises(TypeError, self.recipe.save, 
                          'string instead of Database object')
        # calling save more than once does not increase size of self.db.recipe_keys
        self.recipe.save(self.db)
        self.assertEqual(len(self.db.recipe_keys), length_of_db_recipe_keys)
        # calling save more than once does not increase size of self.category.recipes
        self.assertEqual(len(self.category.recipes), length_of_category_recipes)

    def test_delete(self):
        """Recipe can be deleted"""
        self.assertIsInstance(self.recipe, Recipe)
        self.recipe.save(self.db)
        self.assertEqual(self.recipe, self.db.recipes[self.recipe.key])
        self.assertEqual(self.recipe, self.db.recipes.get(self.recipe.key))
        self.recipe.delete(self.db)
        self.assertRaises(KeyError, utilities.return_value_from_dict,
                          self.db.recipes, self.recipe.key)
        self.assertNotIn(self.recipe.key, self.db.recipe_keys)
        self.assertNotIn(self.recipe.key, self.category.recipes)
        self.assertNotIn(self.recipe.name, self.db.recipe_name_key_map.keys())
        # database parameter should be of type Database
        self.assertRaises(TypeError, self.recipe.delete, 
                          'string instead of Database object')
        # calling delete more than once on same Database objec raises KeyError
        self.assertRaises(KeyError, self.recipe.delete, self.db)

    def test_set_name(self):
        """ The name can be set with a new non-empty string value"""
        # try to set a new name
        new_name = 'foo'
        # save to db
        self.recipe.save(self.db)
        self.recipe.set_name(new_name, self.db)
        # the records in db should be updated also
        self.assertEqual(self.recipe, self.db.recipes[self.recipe.key])
        self.assertIn(self.recipe.key, self.db.recipe_keys)
        self.assertIn(self.recipe.name, self.db.recipe_name_key_map.keys())
        self.assertEqual(self.recipe.key, self.db.recipe_name_key_map[self.recipe.name])
        # assert that the new name is set
        self.assertEqual(new_name, self.recipe.name)
        # try setting with a non string name
        self.assertRaises(TypeError, self.recipe.set_name, 2, self.db)
        # try setting with an empty string
        self.assertRaises(ValueError, self.recipe.set_name, '', self.db)
        # try setting with a space string 
        self.assertRaises(ValueError, self.recipe.set_name, '  ', self.db)
        # try setting with a database that is not a Databas
        self.assertRaises(TypeError, self.recipe.set_name, 'new name',
                          'a string instead of database')

    def test_set_description(self):
        """ The description can be set with a new non-empty string value"""
        # try to set a new description
        new_description = 'bar'
        # Save to self.db
        self.recipe.save(self.db)
        self.recipe.set_description(new_description, self.db)
        self.assertEqual(self.recipe, self.db.recipes[self.recipe.key])
        self.assertIn(self.recipe.key, self.db.recipe_keys)
        self.assertIn(self.recipe.name, self.db.recipe_name_key_map.keys())
        self.assertEqual(self.recipe.key, self.db.recipe_name_key_map[self.recipe.name])
        # assert that the new description is set
        self.assertEqual(new_description, self.recipe.description)
        # try setting with a non string description
        self.assertRaises(TypeError, self.recipe.set_description, 2, self.db)
        # the records in db should be updated also
        # try setting with a database that is not a Databas
        self.assertRaises(TypeError, self.recipe.set_description, 'new description',
                          'a string instead of database')

    def test_recipe_can_create_steps(self):
        """Recipe can create steps under it"""
        self.recipe.save(self.db)
        recipe_step = self.recipe.create_step(self.db, self.recipe_step_data)
        self.assertIsInstance(recipe_step, RecipeStep)
        self.assertIn(recipe_step.key, self.recipe.recipe_steps)
        self.assertIn(recipe_step.key, self.db.recipe_step_keys)
        self.assertEqual(recipe_step, self.db.recipe_steps[recipe_step.key])
        self.assertRaises(TypeError, self.recipe.create_step, 
                          'database should be a Database object', self.recipe_step_data)
        del(self.recipe_step_data['text_content'])
        recipe_step = self.recipe.create_step(self.db, self.recipe_step_data)
        self.assertIsNone(recipe_step)

    def test_get_all_steps(self):
        """The get_all_steps function should be able to retrieve all steps"""
        text_content_tuple = ('Get wheat flour', 'Put salt in water', 'Bake in oven')
        # create three recipe steps
        created_recipe_steps = []
        # incase a recipe step is ever created in the Setup
        key = 2
        # save recipe in db
        self.recipe.save(self.db)
        for text_content in text_content_tuple:
            new_data = utilities.replace_value_in_dict(self.recipe_step_data,
                                                       'text_content', text_content)
            new_recipe_step = RecipeStep(**new_data, key=key, recipe=self.recipe.key)
            new_recipe_step.save(self.db)
            created_recipe_steps.append(new_recipe_step)
            key += 1

        recipe_steps = self.recipe.get_all_steps(self.db)
        self.assertIsInstance(recipe_steps, list)
        self.assertEqual(len(self.recipe.recipe_steps), len(recipe_steps))
        self.assertListEqual(created_recipe_steps, recipe_steps)
        self.assertRaises(TypeError, self.recipe.get_all_steps,
                          'expected Database object not string')


if __name__ == '__main__':
    unittest.main()