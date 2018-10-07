import unittest
import json
import os
from app.test.base import BaseTestCase

# Load all example API objects to be tested
script_dir = os.path.dirname(__file__)

analysis_grid = json.loads(
    open(script_dir + '/resources/analysis_grids/analysis_grid.json').read()
)

surface_with_states = json.loads(
    open(script_dir + '/resources/honeybee_surfaces/surface_with_states.json')
    .read()
)


# API Endpoint testing utility functions
def create_analysis_grid(self, object_data):
    return self.client.post(
        '/analysis_grid/',
        data=json.dumps(object_data),
        content_type='application/json'
    )


def get_analysis_grid(self, object_id):
    return self.client.get(
        '/analysis_grid/' + object_id
    )


def create_honeybee_surface(self, object_data):
    return self.client.post(
        '/honeybee_surface/',
        data=json.dumps(object_data),
        content_type='application/json'
    )


class TestAnalysisGridCRUD(BaseTestCase):
    def test_analysis_grid_crud(self):
        """ Test for analysis grid creation """
        self.maxDiff = None
        with self.client:
            response = create_honeybee_surface(self, surface_with_states)
            data = json.loads(response.data.decode())
            analysis_grid['window_groups'].append({
                'id': data['id']
            })
            response = create_analysis_grid(self, analysis_grid)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            analysis_grid['id'] = data['id']
            response = get_analysis_grid(self, analysis_grid['id'])
            data = json.loads(response.data.decode())
            self.assertEqual(data['id'], analysis_grid['id'])
            self.assertEqual(data['name'], analysis_grid['name'])

            # Check surface group data
            self.assertEqual(len(data['window_groups']),
                             len(analysis_grid['window_groups']))
            # Check analysis points
            self.assertListEqual(data['analysis_points'],
                                 analysis_grid['analysis_points'])


if __name__ == '__main__':
    unittest.main()
