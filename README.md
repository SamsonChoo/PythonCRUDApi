# PythonCRUDApi

A Python REST API built with flask, connected to MySQL Database, that allows user registration, login, and CRUD operations on different shapes. User may perform CRUD operations on the following shapes, in addition to fetching their area and perimeter (computed dynamically):

- Rectangle
- Triangle
- Square
- Diamond

## System

---

This repository was developed with the system versions below:

- Python 3.6.9
- pip 20.2.4
- Windows Subsystem for Linux (WSL) 2
- Ubuntu 18.04.5 LTS

## How to use

---

### Before you start

Download this repository to your local machine using git clone or by downloading the zipped file. Ensure that you have Python3 and pip installed. I would highly suggest working on a virtual environment.

### Installation

```
pip install -r requirements.txt
```

### Setup

Clone your .env.template to a new file and rename it '.env'. Fill in the credentials below:

- DB_TYPE: Your database type (e.g mysql)

- DB_HOST: Where your database is hosted (e.g localhost)

- DB_USER, DB_PASSWORD: Credentials for database login

- DB_SCHEMA: Name of your schema

- DB_SCHEMA_TEST: Name of your test schema (best to keep it seperate)

- FLASK_ENV: Can be 'development' or 'production'

- SECRET_KEY: Enter a random string for the secret key (I suggest using a 256-bit key)

### Setup the database

First Delete the whole _migrations_ folder. Then run the following commands:

```
python3 -m flask db init
python3 -m flask db migrate -m 'Setup Database'
python3 -m flask db upgrade
```

### Start the API server

```
python3 -m flask run
```

### Run tests

```
python3 -m test.main
```

## Questions / Feedbacks / Bugs

---

Feel free to reach out to me if you have any doubts or questions or feedback on how my code can be improved! Pull Requests greatly welcomed too!

## APIs

---

Refer to app/api for details of the APIs. Refer to test for examples of calling them. I would suggest using Postman to call these APIs.

#### Users

Register User: `POST /api/users/register`

- **Params**  
  Required

  - user_name
  - password

  Optional

  - email
  - first_name
  - last_name

- **Returns**
  - user_id
  - user_name
  - email
  - first_name
  - last_name
  - \_links
    - self_by_user_name
    - self_by_user_id
    - update_self_by_user_name
    - update_self_by_user_id
    - create_rectangle
    - create_triangle
    - create_square
    - create_diamond

Login User: `GET /api/login`

- **Headers**  
  Basic Authentication

  - user_name : password

- **Returns**
  - token

Logout User: `DELETE /api/logout`

- **Headers**  
  Token Bearer Authorization

  - token

Get User by user_id: `GET /api/users/<int:user_id>`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**
  - user_id
  - user_name
  - email
  - first_name
  - last_name
  - \_links
    - self_by_user_name
    - self_by_user_id
    - update_self_by_user_name
    - update_self_by_user_id
    - create_rectangle
    - create_triangle
    - create_square
    - create_diamond

Get User by user_name: `GET /api/users/<string:user_name>`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**
  - user_id
  - user_name
  - email
  - first_name
  - last_name
  - \_links
    - self_by_user_name
    - self_by_user_id
    - update_self_by_user_name
    - update_self_by_user_id
    - create_rectangle
    - create_triangle
    - create_square
    - create_diamond

Update User by user_id: `PUT /api/users/<int:user_id>`

- **Headers**  
  Token Bearer Authorization

  - token

- **Params**  
  Optional

  - user_name
  - password
  - email
  - first_name
  - last_name

- **Returns**
  - user_id
  - user_name
  - email
  - first_name
  - last_name
  - \_links
    - self_by_user_name
    - self_by_user_id
    - update_self_by_user_name
    - update_self_by_user_id
    - create_rectangle
    - create_triangle
    - create_square
    - create_diamond

Update User by user_name: `PUT /api/users/<string:user_name>`

- **Headers**  
  Token Bearer Authorization

  - token

- **Params**  
  Optional

  - user_name
  - password
  - email
  - first_name
  - last_name

- **Returns**
  - user_id
  - user_name
  - email
  - first_name
  - last_name
  - \_links
    - self_by_user_name
    - self_by_user_id
    - update_self_by_user_name
    - update_self_by_user_id
    - create_rectangle
    - create_triangle
    - create_square
    - create_diamond

Delete User by user_id: `DELETE /api/users/<int:user_id>`

- **Headers**  
  Token Bearer Authorization

  - token

Delete User by user_name: `DELETE /api/users/<string:user_name>`

- **Headers**  
  Token Bearer Authorization

  - token

#### Rectangles

Create Rectangle: `POST /api/rectangles`

- **Headers**  
  Token Bearer Authorization

  - token

- **Params**  
  Required

  - length
  - width

- **Returns**
  - user_id
  - length
  - width
  - rectangle_id
  - \_links
    - owner
    - self
    - area
    - perimeter
    - update
    - delete

Get Rectangle: `GET /api/rectangles/<int:rectangle_id>`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**
  - user_id
  - length
  - width
  - rectangle_id
  - \_links
    - owner
    - self
    - area
    - perimeter
    - update
    - delete

Get Rectangle Area: `GET /api/rectangles/<int:rectangle_id>/area`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**
  - area

Get Rectangle Perimeter: `GET /api/rectangles/<int:rectangle_id>/perimeter`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**
  - perimeter

Update Rectangle: `PUT /api/rectangles/<int:rectangle_id>`

- **Headers**  
  Token Bearer Authorization

  - token

- **Params**  
  Optional

  - length
  - width

- **Returns**
  - user_id
  - length
  - width
  - rectangle_id
  - \_links
    - owner
    - self
    - area
    - perimeter
    - update
    - delete

Delete Rectangle: `PUT /api/rectangles/<int:rectangle_id>`

- **Headers**  
  Token Bearer Authorization

  - token

#### Triangles

Create Triangle: `POST /api/triangles`

- **Headers**  
  Token Bearer Authorization

  - token

- **Params**  
  Required

  - length1
  - length2
  - length3

- **Returns**
  - user_id
  - length1
  - length2
  - length3
  - triangle_id
  - \_links
    - owner
    - self
    - area
    - perimeter
    - update
    - delete

Get Triangle: `GET /api/triangles/<int:triangle_id>`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**

  - user_id
  - length1
  - length2
  - length3
  - triangle_id
  - \_links - owner - self - area - perimeter - update - delete
    Get Triangle Area: `GET /api/triangles/<int:triangle_id>/area`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**
  - area

Get Triangle Perimeter: `GET /api/triangles/<int:triangle_id>/perimeter`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**

  - perimeter
    Update Triangle: `PUT /api/triangles/<int:triangle_id>`

- **Headers**  
  Token Bearer Authorization

  - token

- **Params**  
  Optional

  - length1
  - length2
  - length3

- **Returns**
  - user_id
  - length1
  - length2
  - length3
  - triangle_id
  - \_links
    - owner
    - self
    - area
    - perimeter
    - update
    - delete

Delete Triangle: `PUT /api/triangles/<int:triangle_id>`

- **Headers**  
  Token Bearer Authorization

  - token

#### Squares

Create Square: `POST /api/squares`

- **Headers**  
  Token Bearer Authorization

  - token

- **Params**  
  Required

  - length

- **Returns**
  - user_id
  - length
  - square_id
  - \_links
    - owner
    - self
    - area
    - perimeter
    - update
    - delete

Get Square: `GET /api/squares/<int:square_id>`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**

  - user_id
  - length
  - square_id
  - \_links - owner - self - area - perimeter - update - delete
    Get Square Area: `GET /api/squares/<int:square_id>/area`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**
  - area

Get Square Perimeter: `GET /api/squares/<int:square_id>/perimeter`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**

  - perimeter
    Update Square: `PUT /api/squares/<int:square_id>`

- **Headers**  
  Token Bearer Authorization

  - token

- **Params**  
  Optional

  - length

- **Returns**
  - user_id
  - length
  - square_id
  - \_links
    - owner
    - self
    - area
    - perimeter
    - update
    - delete

Delete Square: `PUT /api/squares/<int:square_id>`

- **Headers**  
  Token Bearer Authorization

  - token

  #### Diamonds

Create Diamond: `POST /api/diamonds`

- **Headers**  
  Token Bearer Authorization

  - token

- **Params**  
  Required

  - diagonal1
  - diagonal2

- **Returns**
  - user_id
  - diagonal1
  - diagonal2
  - diamond_id
  - \_links
    - owner
    - self
    - area
    - perimeter
    - update
    - delete

Get Diamond: `GET /api/diamonds/<int:diamond_id>`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**

  - user_id
  - diagonal1
  - diagonal2
  - diamond_id
  - \_links - owner - self - area - perimeter - update - delete
    Get Diamond Area: `GET /api/diamonds/<int:diamond_id>/area`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**
  - area

Get Diamond Perimeter: `GET /api/diamonds/<int:diamond_id>/perimeter`

- **Headers**  
  Token Bearer Authorization

  - token

- **Returns**

  - perimeter
    Update Diamond: `PUT /api/diamonds/<int:diamond_id>`

- **Headers**  
  Token Bearer Authorization

  - token

- **Params**  
  Optional

  - diagonal1
  - diagonal2

- **Returns**
  - user_id
  - diagonal1
  - diagonal2
  - diamond_id
  - \_links
    - owner
    - self
    - area
    - perimeter
    - update
    - delete

Delete Diamond: `PUT /api/diamonds/<int:diamond_id>`

- **Headers**  
  Token Bearer Authorization

  - token

## References

---

- [The Flask Mega Tutorial, by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Build a CRUD Web App With Python and Flask, by Mbithe Nzomo](https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-three)
- [Flask official documentation](https://flask.palletsprojects.com/en/1.1.x/)
- [And of course, Stack Overflow](https://stackoverflow.com)

## License

---

GNU GENERAL PUBLIC LICENSE Version 3
