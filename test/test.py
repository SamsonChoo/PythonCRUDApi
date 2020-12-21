import unittest
import os
import json
from flask import abort, url_for, jsonify
from flask_testing import TestCase
from dotenv import load_dotenv
from app import create_app, db
from app.models.user import User
import test.constants as constants


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


class TestUser(TestBase):

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
        print(response.json)
        print(response.headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json['user_name'], constants.USER_NAME)
        self.assertEqual(response.json['email'], constants.EMAIL_VALID)
        self.assertEqual(response.json['first_name'], constants.FIRST_NAME)
        self.assertEqual(response.json['last_name'], constants.LAST_NAME)
        self.assertEqual('password' in response.json, False)
        self.assertEqual('password_hash' in response.json, False)


if __name__ == '__main__':
    unittest.main()
