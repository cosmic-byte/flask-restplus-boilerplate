import datetime
import unittest

from .base import BaseTestCase
from ..main.database import db
from ..main.users.user_model import User


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test',
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        auth_token = User.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test',
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        auth_token = User.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8")) == 1)


if __name__ == '__main__':
    unittest.main()
