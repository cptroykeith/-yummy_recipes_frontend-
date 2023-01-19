"""Module with tests for Controller functions"""


import unittest
from app import controller
from werkzeug.datastructures import ImmutableMultiDict


class ControllerTest(unittest.TestCase):
    """Tests for the controller functions"""

    def test_process_form_data(self):
        """
        This transforms the disfigured form data into 
        a normal dict
        """
        # form return ImmutableMultiDict objects
        raw_form_data = {'name': 'John Doe', 'password': 'password', 'email': ''}
        form_data = ImmutableMultiDict(raw_form_data)
        self.assertTrue(isinstance(form_data,ImmutableMultiDict))
        self.assertEqual(controller.process_form_data(dict(form_data)),raw_form_data)
        # if email is a mandatory field and thus not an empty string
        self.assertRaises(ValueError, controller.process_form_data,dict(form_data), 'email')
        # if many fields/keys are mandatory
        required_keys = ('first_name', 'last_name', 'password')
        self.assertRaises(ValueError, controller.process_form_data,dict(form_data), *required_keys)

    def test_process_args_data(self):
        """
        This ensures mandatory keys are passed or else value errors are raised
        """
        # form return ImmutableMultiDict objects
        raw_args_data = {'name': 'John Doe', 'password': 'password', 'email': ''}
        self.assertEqual(controller.process_args_data(raw_args_data),raw_args_data)
        # if email is a mandatory field and thus not an empty string
        self.assertRaises(ValueError, controller.process_args_data,raw_args_data, 'email')
        # if many fields/keys are mandatory and yet don't appear in dict
        required_keys = ('first_name', 'last_name', 'password')
        self.assertRaises(ValueError, controller.process_args_data,raw_args_data, *required_keys)
        # raises TypeError if first argument is not a dict
        self.assertRaises(TypeError, controller.process_args_data, 'string')



if __name__ == '__main__':
    unittest.main()
        
