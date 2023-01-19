"""
Tests for the functions in the utilities module
"""


import unittest
from app import utilities

class UtilitiesTests(unittest.TestCase):
    """
    Class to test the functionality of the functions
    in utilities.py
    """
    
    def test_check_type_return(self):
        """
        check_type returns True when the object is of any type in args
        check_type raises TypeError when the types are different
        check_type raises an error when the type_object is not a type        
        """
        self.assertTrue(utilities.check_type('girl', str))
        self.assertTrue(utilities.check_type('girl', float, int, str))
        self.assertRaises(TypeError, utilities.check_type, 5, bool)
        self.assertRaises(ValueError, utilities.check_type, 5, 9)
    
    def test_check_email_format(self):
        """
        check_email_formart returns True when email is right format
        check_email_format raises a ValueError when email format is wrong
        check_email_format raises a TypeError when email is not string
        """
        self.assertTrue(utilities.check_email_format('tom@example.com'))
        self.assertRaises(ValueError, utilities.check_email_format,
                        'tomexample.com')
        self.assertRaises(TypeError, utilities.check_email_format,
                        56)

    def test_check_password_format(self):
        """
        check_password_format returns True for a String of more characters
        check_password_format raises a ValueError when password string
        is of length less than min_length (default 6)
        check_password_format raises a TypeError when password is not string
        check_password_format raises a TypeError when min_length is not an int
        """
        self.assertTrue(utilities.check_password_format('rango679kiy'))
        self.assertRaises(ValueError, utilities.check_password_format, 'present',
                        10)
        self.assertRaises(TypeError, utilities.check_password_format, 43.5)
        self.assertRaises(TypeError, utilities.check_password_format, 'password',
                        '34r')

    def test_replace_value_in_dict(self):
        """
        replace_value_in_dict returns a new dict with value for key passed changed
        replace_value_in_dict raises TypeError if dict passed in is not dict
        replace_value_in_dict raises KeyError if key in dict is non existent
        """
        original_dict = {'title': 'foo'}
        new_dict = utilities.replace_value_in_dict(original_dict, 'title', 'bar')
        self.assertEqual(new_dict['title'], 'bar')
        self.assertRaises(TypeError, utilities.replace_value_in_dict, the_dict='a string',
                          key='title', new_value='bar')
        self.assertRaises(KeyError, utilities.replace_value_in_dict, the_dict=original_dict,
                          key='random', new_value='bar')

    def test_return_value_from_dict(self):
        """
        return_value_from_dict should return the right value from a dict
        return_value_from_dict should raise TypeError if dict_object passed is not a dict
        return_value_from_dict shoule raise a KeyError if key passed doesnot exist
        """
        dict_object = {'foo': 'bar'}
        value = utilities.return_value_from_dict(dict_object, 'foo')
        self.assertEqual(dict_object['foo'], value)
        self.assertRaises(TypeError, utilities.return_value_from_dict, 'string_not_dict', 'foo')
        self.assertRaises(KeyError, utilities.return_value_from_dict, dict_object, 'non-existent-key')


if __name__ == '__main__':
    unittest.main()