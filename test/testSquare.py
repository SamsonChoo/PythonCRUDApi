import unittest
import os
import json
from flask import abort, url_for, jsonify
from flask_testing import TestCase
from dotenv import load_dotenv
from app import create_app, db
from app.models.square import Square
from app.models.user import User
import test.constants as constants
import base64


class TestBaseSquare(TestCase):

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
        user = User(user_name=constants.USER_NAME,
                    password=constants.PASSWORD_STRONG,
                    token=constants.TOKEN_VALID,
                    token_expiration=constants.TOKEN_EXPIRATION_VALID)
        db.session.add(user)
        db.session.commit()
        self.user_id = user.user_id

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestCreateSquare(TestBaseSquare):

    def test_create_square_success(self):
        """
        Given proper credentials, it should return status code 201 and given credentials
        """
        payload = json.dumps({
            "length": constants.NUMBER_VALID
        })

        response = self.client.post(
            '/api/squares', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json['user_id'], self.user_id)
        self.assertEqual(response.json['length'], constants.NUMBER_VALID)
        self.assertEqual(response.json['_links']['owner'],  url_for(
            'api.get_user_by_user_id', user_id=self.user_id))

    def test_create_square_fail_no_length(self):
        """
        Given no length, it should return status code 400 and proper error message
        """
        payload = json.dumps({
        })

        response = self.client.post(
            '/api/squares', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "must include length field")

    def test_create_square_fail_negative_length(self):
        """
        Given negative length, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "length": constants.NUMBER_NEGATIVE
        })

        response = self.client.post(
            '/api/squares', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "length must be positive")

    def test_create_square_fail_non_number_length(self):
        """
        Given a length not of number type, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "length": constants.NUMBER_NOT
        })

        response = self.client.post(
            '/api/squares', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "length must be a number")


class TestSquare(TestCase):
    """ Base class to insert test square into database """

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
        user = User(user_name=constants.USER_NAME,
                    password=constants.PASSWORD_STRONG,
                    token=constants.TOKEN_VALID,
                    token_expiration=constants.TOKEN_EXPIRATION_VALID)
        db.session.add(user)
        db.session.commit()
        self.user_id = user.user_id
        square = Square(
            user_id=self.user_id, length=constants.NUMBER_VALID)
        db.session.add(square)
        db.session.commit()
        self.rectangle_id = square.rectangle_id

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestGetSquare(TestSquare):

    def test_get_square_success(self):
        """
        Given correct rectangle_id, it should return status code 200 and correct data
        """
        response = self.client.get(
            f'/api/squares/{self.rectangle_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        self.assert200(response)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json['user_id'], self.user_id)
        self.assertEqual(response.json['length'], constants.NUMBER_VALID)
        self.assertEqual(response.json['_links']['owner'],  url_for(
            'api.get_user_by_user_id', user_id=self.user_id))

    def test_get_square_area_success(self):
        """
        Given correct rectangle_id, it should return status code 200 and correct area
        """
        response = self.client.get(
            f'/api/squares/{self.rectangle_id}/area', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        area = constants.NUMBER_VALID * constants.NUMBER_VALID
        self.assert200(response)
        self.assertEqual(response.json['Area'], area)

    def test_get_square_perimeter_success(self):
        """
        Given correct rectangle_id, it should return status code 200 and correct perimeter
        """
        response = self.client.get(
            f'/api/squares/{self.rectangle_id}/perimeter', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        perimeter = constants.NUMBER_VALID * 4
        self.assert200(response)
        self.assertEqual(response.json['Perimeter'], perimeter)


class TestUpdateSquare(TestSquare):
    def test_update_square_success(self):
        """
        Given correct token and params, it should return status code 200 and correct data
        """
        payload = json.dumps({
            "length": constants.NUMBER_VALID2
        })
        response = self.client.put(
            f'/api/squares/{self.rectangle_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert200(response)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json['user_id'], self.user_id)
        self.assertEqual(response.json['length'], constants.NUMBER_VALID2)
        self.assertEqual(response.json['_links']['owner'],  url_for(
            'api.get_user_by_user_id', user_id=self.user_id))

    def test_update_square_fail_negative_length(self):
        """
        Given negative length, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "length": constants.NUMBER_NEGATIVE
        })

        response = self.client.put(
            f'/api/squares/{self.rectangle_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "length must be positive")

    def test_update_square_fail_non_number_length(self):
        """
        Given a length not of number type, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "length": constants.NUMBER_NOT
        })

        response = self.client.put(
            f'/api/squares/{self.rectangle_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "length must be a number")


class TestDeleteSquare(TestSquare):
    def test_delete_square_success(self):
        """
        Given proper credentials, it should return status code 204
        """
        response = self.client.delete(
            f'/api/squares/{self.rectangle_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        self.assertEqual(response.status_code, 204)
