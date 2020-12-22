import unittest
import os
import json
from flask import abort, url_for, jsonify
from flask_testing import TestCase
from dotenv import load_dotenv
from app import create_app, db
from app.models.user import User
import test.constants as constants
import base64


class TestBase(TestCase):

    def create_app(self):

        load_dotenv()

        # pass in test configurations
        config_name = 'test'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI=os.environ.get(
                'SQLALCHEMY_DATABASE_URI_TEST')
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestCreateUser(TestBase):

    def test_create_user_success(self):
        """
        Given proper credentials, it should return status code 201 and given credentials
        """
        payload = json.dumps({
            "user_name": constants.USER_NAME,
            "password": constants.PASSWORD_STRONG,
            "email": constants.EMAIL_VALID,
            "first_name": constants.FIRST_NAME,
            "last_name": constants.LAST_NAME
        })

        response = self.client.post(
            '/api/users/register', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json['user_name'], constants.USER_NAME)
        self.assertEqual(response.json['email'], constants.EMAIL_VALID)
        self.assertEqual(response.json['first_name'], constants.FIRST_NAME)
        self.assertEqual(response.json['last_name'], constants.LAST_NAME)
        self.assertFalse('password' in response.json)
        self.assertFalse('password_hash' in response.json)

    def test_create_user_fail_no_user_name(self):
        """
        Given no user_name, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "password": constants.PASSWORD_STRONG
        })

        response = self.client.post(
            '/api/users/register', headers={"Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "must include user_name and password fields")

    def test_create_user_fail_no_password(self):
        """
        Given no password, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "user_name": constants.USER_NAME
        })

        response = self.client.post(
            '/api/users/register', headers={"Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "must include user_name and password fields")

    def test_create_user_fail_weak_password1(self):
        """
        Given a short password, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "user_name": constants.USER_NAME,
            "password": constants.PASSWORD_WEAK1
        })

        response = self.client.post(
            '/api/users/register', headers={"Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "please enter a stronger password")

    def test_create_user_fail_weak_password2(self):
        """
        Given a weak password, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "user_name": constants.USER_NAME,
            "password": constants.PASSWORD_WEAK2
        })

        response = self.client.post(
            '/api/users/register', headers={"Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "please enter a stronger password")

    def test_create_user_fail_duplicate_user_name(self):
        """
        Given a duplicate user_name, it should return status code 400 and proper error message
        """
        user = User(user_name=constants.USER_NAME,
                    password=constants.PASSWORD_STRONG)
        db.session.add(user)
        db.session.commit()
        payload = json.dumps({
            "user_name": constants.USER_NAME,
            "password": constants.PASSWORD_STRONG
        })

        response = self.client.post(
            '/api/users/register', headers={"Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "please use a different username")

    def test_create_user_fail_duplicate_email(self):
        """
        Given a duplicate email, it should return status code 400 and proper error message
        """
        user = User(user_name=constants.USER_NAME,
                    password=constants.PASSWORD_STRONG,
                    email=constants.EMAIL_VALID)
        db.session.add(user)
        db.session.commit()
        payload = json.dumps({
            "user_name": constants.USER_NAME,
            "password": constants.PASSWORD_STRONG,
            "email": constants.EMAIL_VALID
        })

        response = self.client.post(
            '/api/users/register', headers={"Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "please use a different username")

    def test_create_user_fail_invalid_email(self):
        """
        Given an invalid email, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "user_name": constants.USER_NAME,
            "password": constants.PASSWORD_STRONG,
            "email": constants.EMAIL_INVALID
        })

        response = self.client.post(
            '/api/users/register', headers={"Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "please enter a valid email address")


class TestUserLogin(TestBase):
    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()
        user = User(user_name=constants.USER_NAME,
                    password=constants.PASSWORD_STRONG,
                    email=constants.EMAIL_VALID,
                    first_name=constants.FIRST_NAME,
                    last_name=constants.LAST_NAME)
        db.session.add(user)
        db.session.commit()
        self.user_id = user.user_id

    def test_user_login_success(self):
        """
        Given correct user_name and password, it should return status code 200 and auth token
        """
        credentials = base64.b64encode(f'{constants.USER_NAME}:{constants.PASSWORD_STRONG}'.encode(
        )).decode('utf-8')
        response = self.client.get(
            '/api/login', headers={"Authorization": "Basic " + credentials})
        self.assert200(response)
        self.assertTrue('token' in response.json)

    def test_user_login_fail_no_credentials(self):
        """
        Given no credential, it should return status code 401 and no token
        """
        response = self.client.get(
            '/api/login', headers={"Authorization": "Basic "})
        self.assertEqual(response.status_code, 401)
        self.assertFalse('token' in response.json)

    def test_user_login_fail_wrong_credentials(self):
        """
        Given wrong credentials, it should return status code 401 and no token
        """
        credentials = base64.b64encode(f'{constants.USER_NAME}:{constants.PASSWORD_WEAK1}'.encode(
        )).decode('utf-8')
        response = self.client.get(
            '/api/login', headers={"Authorization": "Basic " + credentials})
        self.assertEqual(response.status_code, 401)
        self.assertFalse('token' in response.json)


class TestUser(TestBase):
    """ Base class to insert test user into database """

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()
        user1 = User(user_name=constants.USER_NAME,
                     password=constants.PASSWORD_STRONG,
                     email=constants.EMAIL_VALID,
                     first_name=constants.FIRST_NAME,
                     last_name=constants.LAST_NAME,
                     token=constants.TOKEN_VALID,
                     token_expiration=constants.TOKEN_EXPIRATION_VALID
                     )
        db.session.add(user1)
        user2 = User(user_name=constants.USER_NAME3,
                     password=constants.PASSWORD_STRONG,
                     email=constants.EMAIL_VALID3
                     )
        db.session.add(user2)
        db.session.commit()
        self.user_id = user1.user_id


class TestGetUser(TestUser):

    def test_get_user_success(self):
        """
        Given correct token, it should return status code 200 and correct data
        """
        response = self.client.get(
            f'/api/users/{self.user_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        self.assert200(response)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json['user_name'], constants.USER_NAME)
        self.assertEqual(response.json['email'], constants.EMAIL_VALID)
        self.assertEqual(response.json['first_name'], constants.FIRST_NAME)
        self.assertEqual(response.json['last_name'], constants.LAST_NAME)
        self.assertEqual(response.json['_links']['self_by_user_id'], url_for(
            'api.get_user_by_user_id', user_id=self.user_id))
        self.assertEqual(response.json['_links']['self_by_user_name'], url_for(
            'api.get_user_by_user_name', user_name=constants.USER_NAME))
        self.assertFalse('password' in response.json)
        self.assertFalse('password_hash' in response.json)

    def test_get_user_fail_no_token(self):
        """
        Given no token, it should return status code 401 and proper error message
        """
        response = self.client.get(
            f'/api/users/{self.user_id}')
        self.assert401(response)
        self.assertEqual(response.json['error'], 'Unauthorized')

    def test_get_user_fail_invalid_token(self):
        """
        Given invalid token, it should return status code 401 and proper error message
        """
        response = self.client.get(
            f'/api/users/{self.user_id}', headers={"Authorization": "Bearer " + constants.TOKEN_INVALID})
        self.assert401(response)
        self.assertEqual(response.json['error'], 'Unauthorized')

    def test_get_user_fail_wrong_user(self):
        """
        Given unauthorized user id, it should return status code 401 and proper error message
        """
        response = self.client.get(
            f'/api/users/{self.user_id + 1}', headers={"Authorization": "Bearer " + constants.TOKEN_INVALID})
        self.assert401(response)
        self.assertEqual(response.json['error'], 'Unauthorized')


class TestUpdateUser(TestUser):
    def test_update_user_success(self):
        """
        Given correct token and params, it should return status code 200 and correct data
        """
        payload = json.dumps({
            "user_name": constants.USER_NAME2,
            "password": constants.PASSWORD_STRONG,
            "email": constants.EMAIL_VALID2,
            "first_name": constants.FIRST_NAME2,
            "last_name": constants.LAST_NAME2
        })
        response = self.client.put(
            f'/api/users/{self.user_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert200(response)
        self.assertEqual(
            response.headers['Content-Type'], 'application/json')
        self.assertEqual(
            response.json['user_name'], constants.USER_NAME2)
        self.assertEqual(response.json['email'], constants.EMAIL_VALID2)
        self.assertEqual(
            response.json['first_name'], constants.FIRST_NAME2)
        self.assertEqual(
            response.json['last_name'], constants.LAST_NAME2)
        self.assertEqual(response.json['_links']['self_by_user_id'], url_for(
            'api.get_user_by_user_id', user_id=self.user_id))
        self.assertEqual(response.json['_links']['self_by_user_name'], url_for(
            'api.get_user_by_user_name', user_name=constants.USER_NAME2))
        self.assertFalse('password' in response.json)
        self.assertFalse('password_hash' in response.json)

    def test_update_user_fail_duplicate_user_name(self):
        """
        Given duplicate user_name, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "user_name": constants.USER_NAME3,
            "password": constants.PASSWORD_STRONG,
            "email": constants.EMAIL_VALID2,
            "first_name": constants.FIRST_NAME2,
            "last_name": constants.LAST_NAME2
        })
        response = self.client.put(
            f'/api/users/{self.user_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         'please use a different username')

    def test_update_user_fail_duplicate_email(self):
        """
        Given duplicate email, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "user_name": constants.USER_NAME2,
            "password": constants.PASSWORD_STRONG,
            "email": constants.EMAIL_VALID3,
            "first_name": constants.FIRST_NAME2,
            "last_name": constants.LAST_NAME2
        })
        response = self.client.put(
            f'/api/users/{self.user_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         'please use a different email address')

    def test_update_user_fail_duplicate_email(self):
        """
        Given a weak password, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "user_name": constants.USER_NAME2,
            "password": constants.PASSWORD_WEAK1,
            "email": constants.EMAIL_VALID2,
            "first_name": constants.FIRST_NAME2,
            "last_name": constants.LAST_NAME2
        })
        response = self.client.put(
            f'/api/users/{self.user_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         'please enter a stronger password')


class TestDeleteUser(TestUser):
    def test_delete_user_success(self):
        """
        Given proper credentials, it should return status code 204
        """
        response = self.client.delete(
            f'/api/users/{self.user_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        self.assertEqual(response.status_code, 204)

    def test_delete_user_fail_wrong_user(self):
        """
        Given user id that does not belong to user, it should return status code 403
        """
        response = self.client.delete(
            f'/api/users/{self.user_id + 1}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        self.assert403(response)
