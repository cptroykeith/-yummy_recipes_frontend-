"""
This module holds functionality that connects the models to the views
"""
from flask import session
from app.models import db
from app import utilities

def process_form_data(dict_form_data, *args):
    """ 
    After casting form data to dict, the values 
    become lists. Transform the lists to non-iterables
    """
    new_dict = {}
    try:
        for key in dict_form_data.keys():
            new_dict[key] = dict_form_data[key]
    except AttributeError:
        raise AttributeError('The input should be a dictionary')
    # check for mandatory fields as directed by args
    for arg in args:
        try:
            value = new_dict[arg]
            if isinstance(value, str):
                if len(value.strip()) == 0:
                    raise ValueError('%s should not be an empty string' % str(arg))
        except KeyError:
            raise ValueError('%s is an expected key' % str(arg))
    return new_dict

def process_args_data(dict_args_data, *args):
    """ 
    Raise ValueError if mandatory values are empty strings or
    non-existent
    """
    if utilities.check_type(dict_args_data, dict):
        for arg in args:
            try:
                value = dict_args_data[arg]
                if isinstance(value, str):
                    if len(value.strip()) == 0:
                        raise ValueError('%s should not be an empty string' % str(arg))
            except KeyError:
                raise ValueError('%s is an expected key' % str(arg))
        return dict_args_data


def get_logged_in_user_key():
    """
    This checks the session and gets the logged in user's key
    """
    if 'user_key' in session.keys():
        return session['user_key']
    else:
        return None  


def remove_user_from_session():
    """
    Removes the session variable user_key
    from the session to logout the user
    """
    if 'user_key' in session.keys():
        session.pop('user_key')
        session.modified = True
    else:
        raise KeyError('User does not exist in the session')


def add_user_to_session(user_key):
    """
    Adds the session variable user_key for 
    logged in user
    """
    user = db.get_user(user_key)
    if user is None:
        raise KeyError('User does not exist')

    session['user_key'] = user_key
    session.modified = True
    