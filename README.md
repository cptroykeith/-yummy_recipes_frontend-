##Yummy Recipes Frontend
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/cptroykeith/-yummy_recipes_frontend-/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/cptroykeith/-yummy_recipes_frontend-/tree/main)

A web app to save and share food recipes we love.

## About

The YummyRecipes app is a web application meant to help users save and share recipes of their favourite food.

## Interesting Feature
This web app is built using Flask without a database per se. All data is stored in memory (thus the need for only one worker on the server). 

**Fun fact:** A **'Database'** has been implemented within it using python data structures and types. Find the implementation in /flask_app/app/models.py. And yes! It feels like one, it acts like one, it should thus be one. It is a database! 


## Dependencies
1. Bootstrap v4.0.0-alpha
2. Jquery v3.2.1
3. popper.js v1.11.1+
4. Flask v0.12+
5. Python v3.5+

_Other dependecies can be found in requirements.txt in this repo_

# Important Links


## How to run flask application
1. Clone the repository to your computer

    ```
    git clone https://github.com/cptroykeith/-yummy_recipes_frontend-.git
    ```
2. In your terminal, enter the directory YummyRecipes

    ```
    cd YummyRecipes
    ```
3. Create and activate your virtualenv. For ubuntu users, see below.

    ```
    virtualenv -p /usr/bin/python3 env

    source env/bin/activate
    ```
4. Install the packages in requirements.txt

    ``` pip install -r requirements.txt ```

5. To start the app, run the following commands in succession still in the same directory

    ```export FLASK_APP=flask_app/run.py```

    ```export APP_SETTINGS="development"```

    ```export SECRET="the-development-key-secret-hide-very-far"```

    ```flask run ```

    _On windows, use 'set' instead of 'export'_


## How to test the flask appliaction
1. Clone the repository to your computer (as shown above)
2. Ensure you have the dependencies on your system (install the packages in requirements.txt)
3. In your terminal, enter the directory YummyRecipes

    ``` 
    sh -c 'cd ./flask_app/ && coverage run -m --source=app unittest discover test && coverage report'
    ```
4. Observe the output in your terminal
