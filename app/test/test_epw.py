import unittest

import os
import json

from app.test.base import BaseTestCase

# Load all example API objects to be tested
script_dir = os.path.dirname(__file__)

epw = json.loads(
    open(script_dir + '/resources/epws/allahabad.json').read()
)


def create_epw(self, object_data):
    return self.client.post(
        '/epw/',
        data=json.dumps(object_data),
        content_type='application/json'
    )


def get_epw(self, object_id):
    return self.client.get(
        '/epw/' + object_id
    )


class TestEPWCRUD(BaseTestCase):
    def test_create_epw(self):
        """ Test for epw creation """
        with self.client:
            response = create_epw(self, epw)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            epw['id'] = data['id']
            response = get_epw(self, epw['id'])
            data = json.loads(response.data.decode())
            # TODO: Write better equality test to check data inside is correct
            self.assertEqual(data['id'], epw['id'])


if __name__ == '__main__':
    unittest.main()
