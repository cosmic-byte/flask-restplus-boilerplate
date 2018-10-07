import unittest
import json
import os
from app.test.base import BaseTestCase

# Load all example API objects to be tested
script_dir = os.path.dirname(__file__)

material = json.loads(
    open(script_dir + '/resources/materials/opaque.json').read()
)

basic_surface = json.loads(
    open(script_dir + '/resources/honeybee_surfaces/basic_surface.json').read()
)

surface_with_states = json.loads(
    open(script_dir + '/resources/honeybee_surfaces/surface_with_states.json')
    .read()
)


# API Endpoint testing utility functions
def create_honeybee_surface(self, object_data):
    return self.client.post(
        '/honeybee_surface/',
        data=json.dumps(object_data),
        content_type='application/json'
    )


def get_honeybee_surface(self, object_id):
    return self.client.get(
        '/honeybee_surface/' + object_id
    )


def create_material(self, object_data):
    return self.client.post(
        '/material/',
        data=json.dumps(object_data),
        content_type='application/json'
    )


class TestHoneybeeSurfaceCRUD(BaseTestCase):
    def test_simple_surface_crud(self):
        """ Test for basic honeybee surface creation """
        self.maxDiff = None
        with self.client:
            response = create_honeybee_surface(self, basic_surface)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            basic_surface['id'] = data['id']
            response = get_honeybee_surface(self, basic_surface['id'])
            data = json.loads(response.data.decode())
            self.assertEqual(data['id'], basic_surface['id'])
            self.assertEqual(data['name'], basic_surface['name'])
            self.assertEqual(data['type'], basic_surface['type'])

            # Check surface material data
            self.assertEqual(data['radiance_material']['xml_data'],
                             basic_surface['radiance_material']['xml_data'])
            self.assertEqual(data['radiance_material']['up_orientation'],
                             basic_surface['radiance_material']['up_orientation'])
            self.assertEqual(data['radiance_material']['thickness'],
                             basic_surface['radiance_material']['thickness'])
            self.assertEqual(data['radiance_material']['modifier'],
                             basic_surface['radiance_material']['modifier'])
            self.assertEqual(data['radiance_material']['green'], None)

            # Check vertices
            self.assertListEqual(data['vertices'], basic_surface['vertices'])

    def test_surface_with_material_id(self):
        """ Test for basic honeybee surface creation using a material id """
        with self.client:
            material_response = create_material(self, material)
            material_data = json.loads(material_response.data.decode())
            material_id = material_data['id']
            basic_surface['radiance_material'] = {
                "id": material_id
            }

            response = create_honeybee_surface(self, basic_surface)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            basic_surface['id'] = data['id']
            response = get_honeybee_surface(self, basic_surface['id'])
            data = json.loads(response.data.decode())

            # Check surface material data
            self.assertEqual(data['radiance_material']['name'],
                             material['name'])

    def test_material_with_states(self):
        """ Test for creation of honeybee surface with states """
        with self.client:
            material_response = create_material(self, material)
            material_data = json.loads(material_response.data.decode())
            material_id = material_data['id']
            state_from_material_id = {
                "name": "state from material id",
                "type": "window",
                "radiance_material": {
                    "id": material_id
                }
            }
            surface_with_states['states'].append(state_from_material_id)

            response = create_honeybee_surface(self, surface_with_states)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            surface_with_states['id'] = data['id']
            response = get_honeybee_surface(self, surface_with_states['id'])
            data = json.loads(response.data.decode())
            self.assertEqual(data['id'], surface_with_states['id'])
            self.assertEqual(data['name'], surface_with_states['name'])
            self.assertEqual(data['type'], surface_with_states['type'])

            # Check surface material data
            self.assertEqual(data['radiance_material']['name'],
                             surface_with_states['radiance_material']['name'])

            # Check vertices
            self.assertListEqual(data['vertices'], surface_with_states['vertices'])

            # Check states
            self.assertEqual(data['states'][0]['name'],
                             surface_with_states['states'][0]['name'])
            self.assertEqual(data['states'][1]['name'],
                             surface_with_states['states'][1]['name'])


if __name__ == '__main__':
    unittest.main()
