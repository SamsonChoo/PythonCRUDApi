import unittest
import os
import json
from flask import abort, url_for, jsonify
from flask_testing import TestCase
from dotenv import load_dotenv
from app import create_app, db
from app.models.diamond import Diamond
from app.models.user import User
import test.constants as constants
import base64
import math


class TestBaseDiamond(TestCase):

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


class TestCreateDiamond(TestBaseDiamond):

    def test_create_diamond_success(self):
        """
        Given proper credentials, it should return status code 201 and given credentials
        """
        payload = json.dumps({
            "diagonal1": constants.NUMBER_VALID,
            "diagonal2": constants.NUMBER_VALID
        })

        response = self.client.post(
            '/api/diamonds', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json['user_id'], self.user_id)
        self.assertEqual(response.json['diagonal1'], constants.NUMBER_VALID)
        self.assertEqual(response.json['diagonal2'], constants.NUMBER_VALID)
        self.assertEqual(response.json['_links']['owner'],  url_for(
            'api.get_user_by_user_id', user_id=self.user_id))

    def test_create_diamond_fail_no_diagonal1(self):
        """
        Given no diagonal1, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "diagonal2": constants.NUMBER_VALID
        })

        response = self.client.post(
            '/api/diamonds', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "must include diagonal1 and diagonal2 fields")

    def test_create_diamond_fail_no_diagonal2(self):
        """
        Given no diagonal1, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "diagonal1": constants.NUMBER_VALID
        })

        response = self.client.post(
            '/api/diamonds', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "must include diagonal1 and diagonal2 fields")

    def test_create_diamond_fail_negative_diagonal1(self):
        """
        Given negative diagonal1, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "diagonal1": constants.NUMBER_NEGATIVE,
            "diagonal2": constants.NUMBER_VALID
        })

        response = self.client.post(
            '/api/diamonds', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "diagonal1 and diagonal2 must be positive")

    def test_create_diamond_fail_non_number_diagonal1(self):
        """
        Given a diagonal1 not of number type, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "diagonal1": constants.NUMBER_NOT,
            "diagonal2": constants.NUMBER_VALID
        })

        response = self.client.post(
            '/api/diamonds', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "diagonal1 and diagonal2 must be numbers")


class TestDiamond(TestCase):
    """ Base class to insert test diamond into database """

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
        diamond = Diamond(
            user_id=self.user_id, diagonal1=constants.NUMBER_VALID, diagonal2=constants.NUMBER_VALID)
        db.session.add(diamond)
        db.session.commit()
        self.diamond_id = diamond.diamond_id

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestGetDiamond(TestDiamond):

    def test_get_diamond_success(self):
        """
        Given correct diamond_id, it should return status code 200 and correct data
        """
        response = self.client.get(
            f'/api/diamonds/{self.diamond_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        self.assert200(response)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json['user_id'], self.user_id)
        self.assertEqual(response.json['diagonal1'], constants.NUMBER_VALID)
        self.assertEqual(response.json['diagonal2'], constants.NUMBER_VALID)
        self.assertEqual(response.json['_links']['owner'],  url_for(
            'api.get_user_by_user_id', user_id=self.user_id))

    def test_get_diamond_area_success(self):
        """
        Given correct diamond_id, it should return status code 200 and correct area
        """
        response = self.client.get(
            f'/api/diamonds/{self.diamond_id}/area', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        area = constants.NUMBER_VALID * constants.NUMBER_VALID / 2
        self.assert200(response)
        self.assertEqual(response.json['Area'], area)

    def test_get_diamond_perimeter_success(self):
        """
        Given correct diamond_id, it should return status code 200 and correct perimeter
        """
        response = self.client.get(
            f'/api/diamonds/{self.diamond_id}/perimeter', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        perimeter = 2 * math.sqrt(constants.NUMBER_VALID **
                                  2 + constants.NUMBER_VALID ** 2)
        self.assert200(response)
        self.assertEqual(response.json['Perimeter'], perimeter)


class TestUpdateDiamond(TestDiamond):
    def test_update_diamond_success(self):
        """
        Given correct token and params, it should return status code 200 and correct data
        """
        payload = json.dumps({
            "diagonal1": constants.NUMBER_VALID2
        })
        response = self.client.put(
            f'/api/diamonds/{self.diamond_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert200(response)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json['user_id'], self.user_id)
        self.assertEqual(response.json['diagonal1'], constants.NUMBER_VALID2)
        self.assertEqual(response.json['diagonal2'], constants.NUMBER_VALID)
        self.assertEqual(response.json['_links']['owner'],  url_for(
            'api.get_user_by_user_id', user_id=self.user_id))

    def test_update_diamond_fail_negative_diagonal1(self):
        """
        Given negative diagonal1, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "diagonal1": constants.NUMBER_NEGATIVE
        })

        response = self.client.put(
            f'/api/diamonds/{self.diamond_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "diagonal1 and diagonal2 must be positive")

    def test_update_diamond_fail_non_number_diagonal1(self):
        """
        Given a diagonal1 not of number type, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "diagonal1": constants.NUMBER_NOT
        })

        response = self.client.put(
            f'/api/diamonds/{self.diamond_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "diagonal1 and diagonal2 must be numbers")


class TestDeleteDiamond(TestDiamond):
    def test_delete_diamond_success(self):
        """
        Given proper credentials, it should return status code 204
        """
        response = self.client.delete(
            f'/api/diamonds/{self.diamond_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        self.assertEqual(response.status_code, 204)
