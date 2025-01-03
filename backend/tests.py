#!/usr/bin/env python
import unittest

from app import create_app, db
from app.models import Event, User
from config import Config
from datetime import datetime


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username="susan", email="susan@example.com")
        u.set_password("cat")
        self.assertFalse(u.check_password("dog"))
        self.assertTrue(u.check_password("cat"))


class EventModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_from_jasmine_datetime(self):
        datetime_obj = Event.from_jasmine_datetime("2018-06-12T19:30")
        self.assertNotEqual(datetime_obj, datetime(2018, 4, 12, 19, 30))
        self.assertEqual(datetime_obj, datetime(2018, 6, 12, 19, 30))

    def test_to_jasmine_datetime(self):
        datetime_str = Event.to_jasmine_datetime(datetime(2011, 11, 4, 0, 5, 23))
        self.assertNotEqual(datetime_str, "Fri, 04 Nov 2011 00:05:23 GMT")
        self.assertEqual(datetime_str, "2011-11-04T00:05:23")


if __name__ == "__main__":
    unittest.main(verbosity=2)
