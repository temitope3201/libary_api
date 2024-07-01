# recipe_api_x
Library api is a simple rest api built with Django Rest Framework(Python) for Mastering Backend Bootcamp 2.0 project

This recipe api uses swagger ui:
/swagger/
/redoc/

dependencies:
1. django
2. djangorestframework
3. simple_jwt
4. setuptools
5. drf_spectacular

To run on local host

1. git clone 
2. cd lib_api
3. create venv
4. pip install -r requirements.txt
5. python3 manage.py makemigrations
6. python3 manage.py migrate
7. python3 manage.py runserver
8. go-to localhost:8000/api/swagger/
