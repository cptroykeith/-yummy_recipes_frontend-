"""Module with all tests for the RecipeStep class"""


import unittest
from app.models import Database, User, RecipeCategory, \
Recipe, RecipeStep
from app import utilities

class RecipeStepTest(unittest.TestCase):
    """All tests for the RecipeStep class"""
    
    def setUp(self):
        """Initiates variables to be used in most tests"""
        self.db = Database()
        self.user_data = {
            'key': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'roy@example.com',
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
        self.recipe.save(self.db)
        self.recipe_step_data = {
            'key': 1,
            'text_content': "Don't do anything",
            'recipe': self.recipe.key
        }
        self.recipe_step = RecipeStep(**self.recipe_step_data)

    def test_text_content_is_mandatory(self):
        """
        In the constructor, the text_content parameter should be 
        a string which is not empty
        """
        self.assertRaises(TypeError, RecipeStep, key=1,recipe=self.recipe.key)
        invalid_data = utilities.replace_value_in_dict(self.recipe_step_data,
                                                       'text_content', 7)
        self.assertRaises(TypeError, RecipeStep, **invalid_data)
        invalid_data = utilities.replace_value_in_dict(self.recipe_step_data,
                                                       'text_content', '')
        self.assertRaises(ValueError, RecipeStep, **invalid_data)
        invalid_data = utilities.replace_value_in_dict(self.recipe_step_data,
                                                       'text_content', '  ')
        self.assertRaises(ValueError, RecipeStep, **invalid_data)

    def test_save_method(self):
        """
        The save() method should be able to update the parent recipe's 
        list of recipe_steps as well as that of the database
        """
        self.assertIsInstance(self.recipe_step, RecipeStep)
        self.recipe_step.save(self.db)
        length_of_db_recipe_step_keys = len(self.db.recipe_step_keys)
        length_of_recipe_steps = len(self.recipe.recipe_steps)
        self.assertIn(self.recipe_step.key, self.db.recipe_step_keys)
        self.assertEqual(self.recipe_step, self.db.recipe_steps[self.recipe_step.key])
        self.assertIn(self.recipe_step.key, self.recipe.recipe_steps)
        # the recipe should exist in database
        invalid_data = utilities.replace_value_in_dict(self.recipe_step_data, 'recipe', 78)
        new_recipe_step = RecipeStep(**invalid_data)
        self.assertRaises(KeyError, new_recipe_step.save, self.db)
        # database parameter should be of type Database
        self.assertRaises(TypeError, self.recipe_step.save, 
                          'string instead of Database object')
        # calling save more than once does not increase size of self.db.recipe_step_keys
        self.recipe_step.save(self.db)
        self.assertEqual(len(self.db.recipe_step_keys), length_of_db_recipe_step_keys)
        # calling save more than once does not increase size of self.recipe.recipe_steps
        self.assertEqual(len(self.recipe.recipe_steps), length_of_recipe_steps)

    def test_delete(self):
        """RecipeStep object can be deleted"""
        self.assertIsInstance(self.recipe_step, RecipeStep)
        self.recipe_step.save(self.db)
        self.assertEqual(self.recipe_step, self.db.recipe_steps[self.recipe_step.key])
        self.assertEqual(self.recipe_step, self.db.recipe_steps.get(self.recipe_step.key))
        self.recipe_step.delete(self.db)
        self.assertRaises(KeyError, utilities.return_value_from_dict,
                          self.db.recipe_steps, self.recipe_step.key)
        self.assertNotIn(self.recipe_step.key, self.db.recipe_step_keys)
        self.assertNotIn(self.recipe_step.key, self.recipe.recipe_steps)
        # database parameter should be of type Database
        self.assertRaises(TypeError, self.recipe_step.delete, 
                          'string instead of Database object')
        # calling delete more than once on same Database object raises KeyError
        self.assertRaises(KeyError, self.recipe_step.delete, self.db)

    def test_set_text_content(self):
        """ The text_content can be set with a new non-empty string value"""
        # try to set a new name
        new_text = 'Do this instead'
        # save to db
        self.recipe_step.save(self.db)
        self.recipe_step.set_text_content(new_text, self.db)
        # the records in db should be updated also
        self.assertEqual(self.recipe_step, self.db.recipe_steps[self.recipe_step.key])
        self.assertIn(self.recipe_step.key, self.db.recipe_step_keys)
        # assert that the new text content is set
        self.assertEqual(new_text, self.recipe_step.text_content)
        # try setting with a non string name
        self.assertRaises(TypeError, self.recipe_step.set_text_content, 2, self.db)
        # try setting with an empty string
        self.assertRaises(ValueError, self.recipe_step.set_text_content, '', self.db)
        # try setting with a space string 
        self.assertRaises(ValueError, self.recipe_step.set_text_content, '  ', self.db)
        # try setting with a database that is not a Database
        self.assertRaises(TypeError, self.recipe_step.set_text_content, 'blah blah blah',
                          'a string instead of database')


if __name__ == '__main__':
    unittest.main()