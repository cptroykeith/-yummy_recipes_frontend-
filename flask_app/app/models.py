"""
This module holds the pretend-models for the application
"""
from random import randint
from app.utilities import check_type, check_email_format

def binary_search(character, list_of_characters, position=0):
    """
    Searches for character using binary search
    returns None if character is not found
    otherwise returns character's position in sorted list
    """
    length_of_list = len(list_of_characters)
    if length_of_list <= 1:
        if length_of_list == 0:
            return None
        if character != list_of_characters[0]:
            return None
        return position

    random_int = randint(0, length_of_list - 1)
    if character < list_of_characters[random_int]:
        new_list = list_of_characters[:(random_int)]
        position += 0
    else:
        new_list = list_of_characters[random_int:]
        position += random_int
    # return this so that it recursively comes back to the surface
    return binary_search(character, new_list, position)


class Database:
    """This is the daabase for the application"""
    def __init__(self):
        self.users = {}
        self.recipes = {}
        self.recipe_categories = {}
        self.recipe_steps = {}
        self._user_keys = []
        self.user_email_key_map = {}
        self._recipe_keys = []
        self.recipe_name_key_map = {}
        self._recipe_category_keys = []
        self.recipe_category_name_key_map = {}
        self._recipe_step_keys = []

    @property
    def recipe_category_keys(self):
        self._recipe_category_keys =  list(set(self._recipe_category_keys))
        return self._recipe_category_keys

    @property
    def recipe_keys(self):
        self._recipe_keys =  list(set(self._recipe_keys))
        return self._recipe_keys

    @property
    def recipe_step_keys(self):
        self._recipe_step_keys =  list(set(self._recipe_step_keys))
        return self._recipe_step_keys

    @property
    def user_keys(self):
        self._user_keys =  list(set(self._user_keys))
        return self._user_keys

    def get_next_key(self, type_of_object):
        """Gets the next key basing on the type of object"""
        # type_of_object should be of type type
        if check_type(type_of_object, type):
            if type_of_object == User:
                return self.__get_max_value(self.user_keys) + 1

            if type_of_object == Recipe:
                return self.__get_max_value(self.recipe_keys) + 1

            if type_of_object == RecipeCategory:
                return self.__get_max_value(self.recipe_category_keys) + 1

            if type_of_object == RecipeStep:
                return self.__get_max_value(self.recipe_step_keys) + 1

    def __get_max_value(self, unsorted_list):
        """Returns the maximum value of a list or 0 if list is empty"""
        if check_type(unsorted_list, list):
            length = len(unsorted_list)
            if length == 0:
                return 0

            unsorted_list.sort()
            return unsorted_list[length - 1]


    def delete_object(self, object_to_delete):
        """
        Depending on the object type, delete object from
        the dict where its type is
        """
        # store the type of object in a variable
        # check that variable against all the possible
        # Object types and locate the dict
        # then call del(approriate_dict[object_to_delete.key])
        object_type = type(object_to_delete)
        object_dict = {}
        object_keys_list = []
        object_key_map = {}
        object_mapper = ''
        cascaded_objects = []
        if object_type == RecipeCategory:
            object_dict = self.recipe_categories
            object_keys_list = self.recipe_category_keys
            object_key_map = self.recipe_category_name_key_map
            object_mapper = object_to_delete.name
            cascaded_objects = object_to_delete.get_all_recipes(self)

        elif object_type == Recipe:
            object_dict = self.recipes
            object_keys_list = self.recipe_keys
            object_key_map = self.recipe_name_key_map
            object_mapper = object_to_delete.name
            cascaded_objects = object_to_delete.get_all_steps(self)

        elif object_type == RecipeStep:
            object_dict = self.recipe_steps
            object_keys_list = self.recipe_step_keys   

        else:
            raise TypeError('%s type does not exist in database' % str(object_type)) 

        try:
            del(object_dict[object_to_delete.key])
            object_keys_list.remove(object_to_delete.key)
            if object_mapper:
                del(object_key_map[object_mapper])
            # delete child componet objects
            for cascaded_object in cascaded_objects:
                self.delete_object(cascaded_object)
        except KeyError:
            raise KeyError('%s does not exist' % str(object_type))        

    
    def create_user(self, user_data):
        """Creates a new user and adds the user to self.users"""
        try:
            if self.user_email_key_map[user_data['email']]:
                raise ValueError('User already exists')
        except KeyError:
            # if the key does not exist, pass
            pass
        user_key = self.get_next_key(User)
        try:
            user = User(**user_data, key=user_key)
            user.save(self)
        except:
            raise ValueError('invalid user data')
        return user

    def get_user(self, user_key):
        """
        returns the User object corresponding to user_key or
        None if user does not exist
        """
        if check_type(user_key, int):
            try:
                user = self.users[user_key]
            except KeyError:
                return None
            return user

    def get_user_by_email(self, email):
        """
        Returns a user object corresponding to the email
        passed in or None is user does not exist
        """
        if check_type(email, str):
            try:
                user_key = self.user_email_key_map[email]
            except KeyError:
                return None
            return self.get_user(user_key)
        
    def get_recipe_category(self, recipe_category_key):
        """
        Returns the RecipeCategory object if it exists
        or None if it doesn't
        """
        if check_type(recipe_category_key, int):
            try:
                recipe_category = self.recipe_categories[recipe_category_key]
            except KeyError:
                return None
            return recipe_category

    def get_recipe(self, recipe_key):
        """
        Returns the Recipe object if it exists
        or None if it doesn't
        """
        if check_type(recipe_key, int):
            try:
                recipe = self.recipes[recipe_key]
            except KeyError:
                return None
            return recipe

    def get_recipe_step(self, recipe_step_key):
        """
        Returns the RecipeStep object if it exists
        or None if it doesn't
        """
        if check_type(recipe_step_key, int):
            try:
                recipe_step = self.recipe_steps[recipe_step_key]
            except KeyError:
                return None
            return recipe_step


class User:
    """
    Any user who interfaces with the app falls in this category
    """
    def __init__(self, key, first_name, last_name, email, password):
        if check_type(key, int):
            self.key = key
        if check_type(first_name, str):
            self.first_name = first_name
        if check_type(last_name, str):
            self.last_name = last_name
        if check_type(email, str):
            if check_email_format(email):
                self.email = email
        if check_type(password, str):
            self.password = password
        # a list of recipe_category keys
        self._recipe_categories = []

    @property
    def recipe_categories(self):
        self._recipe_categories = list(set(self._recipe_categories))
        return self._recipe_categories

    def add_recipe_category(self, key):
        """Adds a new recipe category key to self._recipe_categories"""
        self._recipe_categories.append(key)

    def save(self, database):
        """Saves user to the database appropriately"""
        # add self's key to db's set of user keys
        # Add self to db.users dict with key as self.key
        if check_type(database, Database):
            database.user_keys.append(self.key)
            database.users[self.key] = self
            database.user_email_key_map[self.email] = self.key

    def create_recipe_category(self, database, recipe_category_data):
        """
        Creates a new recipe category and
        adds it to database.recipe_categories
        """
        if check_type(database, Database):
            # get the last recipe category key and add 1 
            key = database.get_next_key(RecipeCategory)
            try:
                # save user in database
                self.save(database)
                category = RecipeCategory(**recipe_category_data, key=key, user=self.key)
                category.save(database)
            except TypeError:
                return None
            return category

    def get_all_recipe_categories(self, database):
        """Returns all the user's recipe categories"""
        if check_type(database, Database):
            local_recipe_categories = []
            for category in self.recipe_categories:
                try:
                    recipe_category_object = database.recipe_categories[category]
                except KeyError:
                    self.recipe_categories.remove(category)
                else:
                    local_recipe_categories.append(recipe_category_object)

            return local_recipe_categories


class RecipeCategory:
    """
    All categories of recipes belong to this class.
    Each RecipeCategory is created and can be deleted by
    one user
    """
    def __init__(self, key, name, user, description=''):
        if check_type(key, int):
            self.key = key
        if check_type(name, str):
            if len(name.strip()) == 0:
                raise ValueError('name should be a non-empty string')
            self.name = name
        if check_type(description, str):
            self.description = description
        # the creator's key. It does not change
        if check_type(user, int):
            self.user = user
        # the list of child recipe keys
        self._recipes = []

    @property
    def recipes(self):
        self._recipes = list(set(self._recipes))
        return self._recipes

    def delete(self, database):
        """Deletes this category of recipes and all recipes in it"""
        if check_type(database, Database):
            try:
                database.delete_object(self)
                user = database.get_user(self.user)
                if user:
                    user.recipe_categories.remove(self.key)
            except KeyError:
                raise KeyError('The recipe category is non-existent in database')

    def create_recipe(self, database, recipe_data):
        """
        Creates a new recipe and
        adds it to database.recipes
        """
        if check_type(database, Database):
            # get the last recipe key and add 1 
            key = database.get_next_key(Recipe)
            try:
                # save category in database
                self.save(database)
                recipe = Recipe(**recipe_data, key=key, category=self.key)
                recipe.save(database)
            except TypeError:
                return None
            return recipe

    def get_all_recipes(self, database):
        """Returns all recipes under this category"""
        if check_type(database, Database):
            local_recipes = []
            for recipe in self.recipes:
                try:
                    recipe_object = database.recipes[recipe]
                except KeyError:
                    self.recipes.remove(recipe)
                else:
                    local_recipes.append(recipe_object)

            return local_recipes

    def set_description(self, description, database):
        """Edit the description of this recipe category"""
        if check_type(description, str) and check_type(database, Database):
            self.description = description
            self.save(database)

    def set_name(self, name, database):
        """Edit the name of this recipe category"""
        if check_type(name, str) and check_type(database, Database):
            if len(name.strip()) == 0:
                raise ValueError('name should be a non-empty string')
            self.name = name
            self.save(database)

    def save(self, database):
        """Saves recipe category in db and in user"""
        # add self's key to set of recipe categories of user
        if check_type(database, Database):
            try:
                user = database.users[self.user]
                user.recipe_categories.append(self.key)
            except KeyError:
                raise KeyError('User should be saved in db first')
            # add self's key to set of db's recipe_category_keys
            database.recipe_category_keys.append(self.key)
            # Add self to db.recipe_categories dict with key as self.key
            database.recipe_categories[self.key] = self
            # Add self's name and key in db's recipe_category_name_key_map
            database.recipe_category_name_key_map[self.name] = self.key


class Recipe:
    """
    Each recipe are owned by a user and has a category
    """
    def __init__(self, key, name, description, category):
        if check_type(key, int):
            self.key = key
        if check_type(name, str):
            if len(name.strip()) == 0:
                raise ValueError('name should be a non-empty string')
            self.name = name
        if check_type(description, str):
            self.description = description
        # the category key.
        if check_type(category, int):
            self.category = category
        self._recipe_steps = []
        
    @property
    def recipe_steps(self):
        self._recipe_steps = list(set(self._recipe_steps))
        return self._recipe_steps

    def change_category(self, new_category, database):
        """Changes the category of the recipe"""
        # add self's key to new_category's recipe list
        # remove self's key from old category's recipe list
        pass

    def delete(self, database):
        """Deleted the recipe and all its steps"""
        if check_type(database, Database):
            try:
                database.delete_object(self)
                category = database.get_recipe_category(self.category)
                if category:
                    category.recipes.remove(self.key)
            except KeyError:
                raise KeyError('The recipe is non-existent in database')

    def create_step(self, database, recipe_step_data):
        """
        Creates a new recipe step and
        adds it to database.recipe_steps
        """
        if check_type(database, Database):
            # get the last recipe_step key and add 1 
            key = database.get_next_key(RecipeStep)
            try:
                # save recipe in database
                self.save(database)
                recipe_step = RecipeStep(**recipe_step_data, key=key, recipe=self.key)
                recipe_step.save(database)
            except TypeError:
                return None
            return recipe_step

    def get_all_steps(self, database):
        """returns a list of all steps that belong to self"""
        if check_type(database, Database):
            local_recipe_steps = []
            for recipe_step in self.recipe_steps:
                try:
                    recipe_step_object = database.recipe_steps[recipe_step]
                except KeyError:
                    self.recipe_steps.remove(recipe_step)
                else:
                    local_recipe_steps.append(recipe_step_object)

            return local_recipe_steps

    def set_name(self, name, database):
        """Edit the name of this recipe"""
        if check_type(name, str) and check_type(database, Database):
            if len(name.strip()) == 0:
                raise ValueError('name should be a non-empty string')
            self.name = name
            self.save(database)

    def set_description(self, description, database):
        """Edit the description of this recipe"""
        if check_type(description, str) and check_type(database, Database):
            self.description = description
            self.save(database)

    def save(self, database):
        """
        Saves the recipe to the db and to the category's set of recipes
        """
        if check_type(database, Database):
            try:
                category = database.recipe_categories[self.category]
                category.recipes.append(self.key)
            except KeyError:
                raise KeyError('Category should be saved in db first')
            # add self's key to set of db's recipe_keys
            database.recipe_keys.append(self.key)
            # Add self to db.recipes dict with key as self.key
            database.recipes[self.key] = self
            # Add self's name and key in db's recipe_name_key_map
            database.recipe_name_key_map[self.name] = self.key


class RecipeStep:
    """Every recipe contains individual steps"""
    def __init__(self, key,  text_content, recipe):
        if check_type(key, int):
            self.key = key
        if check_type(text_content, str):
            if len(text_content.strip()) == 0:
                raise ValueError('text content should be a non-empty string')
            self.text_content = text_content
        # the recipe key. It does not change
        if check_type(recipe, int):
            self.recipe = recipe
        self.key = key
        self.recipe = recipe
        self.text_content = text_content

    def delete(self, database):
        """Deleted the recipe step"""
        if check_type(database, Database):
            try:
                database.delete_object(self)
                recipe = database.get_recipe(self.recipe)
                if recipe:
                    recipe.recipe_steps.remove(self.key)
            except KeyError:
                raise KeyError('The recipe step is non-existent in database')

    def set_text_content(self, text_content, database):
        """Edit the text_content of this recipe step"""
        if check_type(text_content, str) and check_type(database, Database):
            if len(text_content.strip()) == 0:
                raise ValueError('text_content should be a non-empty string')
            self.text_content = text_content
            self.save(database)

    def save(self, database):
        """
        Save this object's key in parent recipe's set of recipe steps
        and in db
        """
        if check_type(database, Database):
            try:
                recipe = database.recipes[self.recipe]
                recipe.recipe_steps.append(self.key)
            except KeyError:
                raise KeyError('Recipe should be saved in db first')
            # add self's key to set of db's recipe_step_keys
            database.recipe_step_keys.append(self.key)
            # Add self to db.recipe_steps dict with key as self.key
            database.recipe_steps[self.key] = self


# A global db
db = Database()
