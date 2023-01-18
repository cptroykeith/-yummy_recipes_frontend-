"""
This module has functions used across different classes
"""

import re


def check_type(obj, type_object, *args, error_string='Invalid type'):
    """
    Checks the type of obj against the type_object
    and returns True if the same or else raises TypeError
    """
    if not isinstance(type_object, type):
        raise ValueError('second argument of check_type should be\
        a type not a %s')

    if isinstance(obj, type_object):
            return True

    arg_length = len(args)
    if arg_length > 0:
        for item in args:
            if isinstance(obj, item):
                return True

    raise TypeError(error_string)   


def check_email_format(email):
    """
    Checks that the email is in the right format with at
    least one @ and one period (.)
    """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError('Invalid email format')
    return True


def check_password_format(password, min_length=6):
    """
    Checks to ensure that the password is a string of not less
    than min_length
    """
    if check_type(password, str):
        if len(password) < min_length:
            raise ValueError("Your password is too short")
        return True

def replace_value_in_dict(the_dict, key, new_value):
    """Returns a new dict with value replaced"""
    if not isinstance(the_dict, dict):
        raise TypeError('the_dict should be a dict')

    try:
        dict_copy = the_dict
        # this causes function to raise KeyError if key does
        # not exist
        old_value = dict_copy[key]
        dict_copy[key] = new_value
        return dict_copy
    except KeyError:
        raise KeyError('The key does not exist in the_dict')


def return_value_from_dict(dict_object, key):
    """Returns the value at the said key and is able to raise KeyErrors"""
    if check_type(dict_object, dict):
        return dict_object[key]
    else:
        raise TypeError('dict_object should be a dictionary')
