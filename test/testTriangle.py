import unittest
import os
import json
from flask import abort, url_for, jsonify
from flask_testing import TestCase
from dotenv import load_dotenv
from app import create_app, db
from app.models.triangle import Triangle
from app.models.user import User
import test.constants as constants
import base64
import math


class TestBaseTriangle(TestCase):

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


class TestCreateTriangle(TestBaseTriangle):

    def test_create_triangle_success(self):
        """
        Given proper credentials, it should return status code 201 and given credentials
        """
        payload = json.dumps({
            "length1": constants.NUMBER_VALID,
            "length2": constants.NUMBER_VALID,
            "length3": constants.NUMBER_VALID
        })

        response = self.client.post(
            '/api/triangles', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json['user_id'], self.user_id)
        self.assertEqual(response.json['length1'], constants.NUMBER_VALID)
        self.assertEqual(response.json['length2'], constants.NUMBER_VALID)
        self.assertEqual(response.json['length3'], constants.NUMBER_VALID)
        self.assertEqual(response.json['_links']['owner'],  url_for(
            'api.get_user_by_user_id', user_id=self.user_id))

    def test_create_triangle_fail_no_length(self):
        """
        Given no length, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "length1": constants.NUMBER_VALID
        })

        response = self.client.post(
            '/api/triangles', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "must include length1, length2, and length3 fields")

    def test_create_triangle_fail_negative_length(self):
        """
        Given negative length, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "length1": constants.NUMBER_NEGATIVE,
            "length2": constants.NUMBER_VALID,
            "length3": constants.NUMBER_VALID
        })

        response = self.client.post(
            '/api/triangles', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "length must be positive")

    def test_create_triangle_fail_non_number_length(self):
        """
        Given a length not of number type, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "length1": constants.NUMBER_NOT,
            "length2": constants.NUMBER_VALID,
            "length3": constants.NUMBER_VALID
        })

        response = self.client.post(
            '/api/triangles', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "length must be numbers")


class TestTriangle(TestCase):
    """ Base class to insert test triangle into database """

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
        triangle = Triangle(
            user_id=self.user_id, length1=constants.NUMBER_VALID, length2=constants.NUMBER_VALID, length3=constants.NUMBER_VALID)
        db.session.add(triangle)
        db.session.commit()
        self.triangle_id = triangle.triangle_id

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestGetTriangle(TestTriangle):

    def test_get_triangle_success(self):
        """
        Given correct triangle_id, it should return status code 200 and correct data
        """
        response = self.client.get(
            f'/api/triangles/{self.triangle_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        self.assert200(response)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json['user_id'], self.user_id)
        self.assertEqual(response.json['length1'], constants.NUMBER_VALID)
        self.assertEqual(response.json['length2'], constants.NUMBER_VALID)
        self.assertEqual(response.json['length3'], constants.NUMBER_VALID)
        self.assertEqual(response.json['_links']['owner'],  url_for(
            'api.get_user_by_user_id', user_id=self.user_id))

    def test_get_triangle_area_success(self):
        """
        Given correct triangle_id, it should return status code 200 and correct area
        """
        response = self.client.get(
            f'/api/triangles/{self.triangle_id}/area', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        halfPerimeter = (constants.NUMBER_VALID +
                         constants.NUMBER_VALID + constants.NUMBER_VALID) / 2
        area = math.sqrt(halfPerimeter * (halfPerimeter - constants.NUMBER_VALID)
                         * (halfPerimeter - constants.NUMBER_VALID) * (halfPerimeter - constants.NUMBER_VALID))
        self.assert200(response)
        self.assertEqual(response.json['Area'], area)

    def test_get_triangle_perimeter_success(self):
        """
        Given correct triangle_id, it should return status code 200 and correct perimeter
        """
        response = self.client.get(
            f'/api/triangles/{self.triangle_id}/perimeter', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        perimeter = (constants.NUMBER_VALID +
                     constants.NUMBER_VALID + constants.NUMBER_VALID)
        self.assert200(response)
        self.assertEqual(response.json['Perimeter'], perimeter)


class TestUpdateTriangle(TestTriangle):
    def test_update_triangle_success(self):
        """
        Given correct token and params, it should return status code 200 and correct data
        """
        payload = json.dumps({
            "length1": constants.NUMBER_VALID2
        })
        response = self.client.put(
            f'/api/triangles/{self.triangle_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert200(response)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json['user_id'], self.user_id)
        self.assertEqual(response.json['length1'], constants.NUMBER_VALID2)
        self.assertEqual(response.json['length2'], constants.NUMBER_VALID)
        self.assertEqual(response.json['length3'], constants.NUMBER_VALID)
        self.assertEqual(response.json['_links']['owner'],  url_for(
            'api.get_user_by_user_id', user_id=self.user_id))

    def test_update_triangle_fail_negative_length(self):
        """
        Given negative length, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "length1": constants.NUMBER_NEGATIVE
        })

        response = self.client.put(
            f'/api/triangles/{self.triangle_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "length must be positive")

    def test_update_triangle_fail_non_number_length(self):
        """
        Given a length not of number type, it should return status code 400 and proper error message
        """
        payload = json.dumps({
            "length1": constants.NUMBER_NOT
        })

        response = self.client.put(
            f'/api/triangles/{self.triangle_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID, "Content-Type": "application/json"}, data=payload)
        self.assert400(response)
        self.assertEqual(response.json['message'],
                         "length must be numbers")


class TestDeleteTriangle(TestTriangle):
    def test_delete_triangle_success(self):
        """
        Given proper credentials, it should return status code 204
        """
        response = self.client.delete(
            f'/api/triangles/{self.triangle_id}', headers={"Authorization": "Bearer " + constants.TOKEN_VALID})
        self.assertEqual(response.status_code, 204)
