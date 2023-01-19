"""Module to test the User Data Model"""

import unittest
from app.models import User, Database, RecipeCategory
from app import utilities


class UserTest(unittest.TestCase):
    """Tests for the User data model"""

    def setUp(self):
        """
        Set up variables that will be used in most tests
        """
        self.user_data = {
            'key': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'password',
            }
        self.user = User(**self.user_data)
        self.db = Database()
        self.category_data = {
            'name': 'cakes',
            'description': 'all recipes cake!',
        }

    def test_user_can_be_created(self):
        """User can be created"""
        user = User(**self.user_data)
        self.assertIsInstance(user, User)
        self.assertRaises(TypeError, User, key=3)
        del(self.user_data['password'])
        self.assertRaises(TypeError, User, **self.user_data)
    
    def test_first_name_is_string(self):
        """The first name should be a string"""
        invalid_data = utilities.replace_value_in_dict(self.user_data, 'first_name', 3)
        self.assertRaises(TypeError, User, **invalid_data)

    def test_last_name_is_string(self):
        """The last name should be a string"""
        invalid_data = utilities.replace_value_in_dict(self.user_data, 'last_name', 3)
        self.assertRaises(TypeError, User, **invalid_data)

    def test_email_is_string(self):
        """The email should be a string"""
        invalid_data = utilities.replace_value_in_dict(self.user_data, 'email', 3)
        self.assertRaises(TypeError, User, **invalid_data)

    def test_email_is_right_format(self):
        """The email should be in the format xxxx@xxxx.com"""
        invalid_data = utilities.replace_value_in_dict(self.user_data, 'email', 'hello')
        self.assertRaises(ValueError, User, **invalid_data)

    def test_password_is_string(self):
        """The password should be a string"""
        invalid_data = utilities.replace_value_in_dict(self.user_data, 'password', 3)
        self.assertRaises(TypeError, User, **invalid_data)

    def test_key_is_int(self):
        """The key should be an int"""
        invalid_data = utilities.replace_value_in_dict(self.user_data, 'key', 'string_key')
        self.assertRaises(TypeError, User, **invalid_data)

    def test_user_can_be_saved(self):
        """User can be saved in Database"""
        self.assertRaises(TypeError, self.user.save,
                          'Database object expected')
        self.user.save(self.db)
        length_of_user_keys = len(self.db.user_keys)
        self.assertIn(self.user.key, self.db.user_keys)
        self.assertEqual(self.user, self.db.users[self.user.key])
        self.assertIn(self.user.email, self.db.user_email_key_map.keys())
        self.assertEqual(self.user.key, self.db.user_email_key_map[self.user.email])
        # calling save more than once does not increase size of self.db.user_keys
        self.user.save(self.db)
        self.assertEqual(len(self.db.user_keys), length_of_user_keys)

    def test_user_can_create_categories(self):
        """User can create recipe categories"""
        category = self.user.create_recipe_category(self.db, self.category_data)
        self.assertIsInstance(category, RecipeCategory)
        self.assertIn(category.key, self.user.recipe_categories)
        self.assertIn(category.key, self.db.recipe_category_keys)
        self.assertEqual(category, self.db.recipe_categories[category.key])
        self.assertIn(category.name, self.db.recipe_category_name_key_map.keys())
        self.assertEqual(category.key,
                          self.db.recipe_category_name_key_map[category.name])
        self.assertRaises(TypeError, self.user.create_recipe_category, 
                          'database should be a Database object', self.category_data)
        del(self.category_data['name'])
        category = self.user.create_recipe_category(self.db, self.category_data)
        self.assertIsNone(category)
    
    def test_user_can_get_categories(self):
        """User can get a list of their recipe categories"""        
        names = ('cakes', 'bread', 'juice')
        # create three categories
        created_categories = []
        key = 2
        # save user in db
        self.user.save(self.db)
        for name in names:
            new_data = utilities.replace_value_in_dict(self.category_data, 'name', name)
            new_category = RecipeCategory(**new_data, key=key, user=self.user.key)
            new_category.save(self.db)
            created_categories.append(new_category)
            key += 1

        categories = self.user.get_all_recipe_categories(self.db)
        self.assertIsInstance(categories, list)
        self.assertEqual(len(self.user.recipe_categories), len(categories))
        self.assertListEqual(created_categories, categories)
        self.assertRaises(TypeError, self.user.get_all_recipe_categories,
                          'expected Database object not string')


    def test_user_can_delete_categories(self):
        """User can delete recipe categories"""
        pass




if __name__ == '__main__':
    unittest.main()