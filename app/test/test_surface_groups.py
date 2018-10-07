import unittest
import json
import os
from app.test.base import BaseTestCase

# Load all example API objects to be tested
script_dir = os.path.dirname(__file__)

basic_surface = json.loads(
    open(script_dir + '/resources/honeybee_surfaces/basic_surface.json').read()
)

surface_group = json.loads(
    open(script_dir + '/resources/surface_group/surface_group.json')
    .read()
)


# API Endpoint testing utility functions
def create_honeybee_surface(self, object_data):
    return self.client.post(
        '/honeybee_surface/',
        data=json.dumps(object_data),
        content_type='application/json'
    )


def get_surface_group(self, object_id):
    return self.client.get(
        '/surface_group/' + object_id
    )


def create_surface_group(self, object_data):
    return self.client.post(
        '/surface_group/',
        data=json.dumps(object_data),
        content_type='application/json'
    )


class TestSurfaceGroupCRUD(BaseTestCase):
    def test_surface_group_crud(self):
        """ Test for surface group creation """
        self.maxDiff = None
        with self.client:
            response = create_honeybee_surface(self, basic_surface)
            data = json.loads(response.data.decode())
            surface_group['honeybee_surfaces'].append({
                "id": data['id']
            })
            response = create_surface_group(self, surface_group)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            surface_group['id'] = data['id']
            response = get_surface_group(self, surface_group['id'])
            data = json.loads(response.data.decode())
            self.assertEqual(data['id'], surface_group['id'])
            self.assertEqual(data['name'], surface_group['name'])
            self.assertEqual(data['description'], surface_group['description'])

            # Check number of surfaces matches
            self.assertEqual(data['honeybee_surface_count'],
                             len(surface_group['honeybee_surfaces']))


if __name__ == '__main__':
    unittest.main()
