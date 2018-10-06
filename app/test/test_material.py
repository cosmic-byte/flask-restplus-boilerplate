import unittest
import json
import os
from app.test.base import BaseTestCase

# Load all example API objects to be tested
script_dir = os.path.dirname(__file__)

bsdf = json.loads(
    open(script_dir + '/resources/materials/bsdf.json').read())

light_source = json.loads(
    open(script_dir + '/resources/materials/light_source.json').read())

opaque = json.loads(
    open(script_dir + '/resources/materials/opaque.json').read())

translucent = json.loads(
    open(script_dir + '/resources/materials/translucent.json').read())

incorrect = json.loads(
    open(script_dir + '/resources/materials/incorrect.json').read())


# API Endpoint testing utility functions
def create_material(self, object_data):
    return self.client.post(
        '/material/',
        data=json.dumps(object_data),
        content_type='application/json'
    )


def get_material(self, object_id):
    return self.client.get(
        '/material/' + object_id
    )


class TestMaterialCRUD(BaseTestCase):
    def test_bsdf_crud(self):
        """ Test for bsdf material creation """
        self.maxDiff = None
        with self.client:
            response = create_material(self, bsdf)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            bsdf['id'] = data['id']
            response = get_material(self, bsdf['id'])
            data = json.loads(response.data.decode())
            self.assertEqual(data['id'], bsdf['id'])
            self.assertEqual(data['name'], bsdf['name'])
            self.assertEqual(data['type'], bsdf['type'])

            self.assertEqual(data['xml_data'], bsdf['xml_data'])
            self.assertEqual(data['up_orientation'], bsdf['up_orientation'])
            self.assertEqual(data['thickness'], bsdf['thickness'])
            self.assertEqual(data['modifier'], bsdf['modifier'])
            self.assertEqual(data['green'], None)

    def test_light_source_crud(self):
        """ Test for light source material creation """
        self.maxDiff = None
        with self.client:
            response = create_material(self, light_source)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            light_source['id'] = data['id']
            response = get_material(self, light_source['id'])
            data = json.loads(response.data.decode())
            self.assertEqual(data['id'], light_source['id'])
            self.assertEqual(data['name'], light_source['name'])
            self.assertEqual(data['type'], light_source['type'])

            self.assertEqual(data['red'], light_source['red'])
            self.assertEqual(data['green'], light_source['green'])
            self.assertEqual(data['blue'], light_source['blue'])
            self.assertEqual(data['radius'], light_source['radius'])
            self.assertEqual(data['modifier'], light_source['modifier'])
            self.assertEqual(data['xml_data'], None)

    def test_opaque_crud(self):
        """ Test for opaque material creation """
        self.maxDiff = None
        with self.client:
            response = create_material(self, opaque)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            opaque['id'] = data['id']
            response = get_material(self, opaque['id'])
            data = json.loads(response.data.decode())
            self.assertEqual(data['id'], opaque['id'])
            self.assertEqual(data['name'], opaque['name'])
            self.assertEqual(data['type'], opaque['type'])

            self.assertEqual(data['r_reflectance'], opaque['r_reflectance'])
            self.assertEqual(data['g_reflectance'], opaque['g_reflectance'])
            self.assertEqual(data['b_reflectance'], opaque['b_reflectance'])
            self.assertEqual(data['specularity'], opaque['specularity'])
            self.assertEqual(data['roughness'], opaque['roughness'])
            self.assertEqual(data['modifier'], opaque['modifier'])
            self.assertEqual(data['xml_data'], None)

    def test_translucent_crud(self):
        """ Test for translucent material creation """
        self.maxDiff = None
        with self.client:
            response = create_material(self, translucent)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            translucent['id'] = data['id']
            response = get_material(self, translucent['id'])
            data = json.loads(response.data.decode())
            self.assertEqual(data['id'], translucent['id'])
            self.assertEqual(data['name'], translucent['name'])
            self.assertEqual(data['type'], translucent['type'])

            self.assertEqual(data['r_transmittance'],
                             translucent['r_transmittance'])
            self.assertEqual(data['g_transmittance'],
                             translucent['g_transmittance'])
            self.assertEqual(data['b_transmittance'],
                             translucent['b_transmittance'])
            self.assertEqual(data['refraction'], translucent['refraction'])
            self.assertEqual(data['modifier'], translucent['modifier'])
            self.assertEqual(data['xml_data'], None)


if __name__ == '__main__':
    unittest.main()
