import uuid
import datetime

from app.main import db
from app.main.model.analysis_grid import GridPoint, AnalysisGrid
from app.main.model.honeybee_surface import HoneybeeSurface
from app.main.service.honeybee_surface_service import save_new_honeybee_surface,\
                                                      get_a_honeybee_surface, \
                                                      serialize_honeybee_surface


def save_new_analysis_grid(data):
    grid_points = []
    window_groups = []

    for point_data in data['analysis_points']:
        api_response, success = save_new_grid_point(point_data,
                                                    data['user_id'])
        if success:
            grid_points.append(api_response['grid_point'])
        else:
            return api_response, 409

    for window_group_data in data['window_groups']:
        if 'id' not in window_group_data.keys():
            window_group_data['user_id'] = data['user_id']
            api_response, success = \
                save_new_honeybee_surface(window_group_data)
            if success:
                window_group_data['id'] = api_response['id']
            else:
                return api_response, 409
        honeybee_surface = HoneybeeSurface.query\
            .filter_by(id=window_group_data['id']).first()
        window_groups.append(honeybee_surface)

    new_analysis_grid = AnalysisGrid(
        id=str(uuid.uuid4()),
        created_on=datetime.datetime.utcnow(),
        created_by=str(data['user_id']),
        updated_on=datetime.datetime.utcnow(),
        updated_by=str(data['user_id']),

        name=str(data['name']),
        analysis_points=grid_points,
        window_groups=window_groups
        )

    try:
        save_changes(new_analysis_grid)
        response_object = {
            'status': 'success',
            'message': 'sucesfully created analysis grid',
            'id': str(new_analysis_grid.id)
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'failure',
            'message':
                'something went wrong adding new analysis grid to the database',
            'error': str(e)
        }
        return response_object, 409


def save_new_grid_point(data, user_id):
    grid_point = GridPoint(
        id=str(uuid.uuid4()),
        created_on=datetime.datetime.utcnow(),
        created_by=str(user_id),
        updated_on=datetime.datetime.utcnow(),
        updated_by=str(user_id),

        x=data['x'],
        y=data['y'],
        z=data['z'],
        vx=data['vx'],
        vy=data['vy'],
        vz=data['vz']
    )

    try:
        save_changes(grid_point)
        response_object = {
            'status': 'success',
            'message': 'sucesfully created honeybee surface',
            'grid_point': grid_point
        }
        return response_object, True
    except Exception as e:
        response_object = {
            'status': 'failure',
            'message':
                'something went wrong adding new grid point to the database',
            'error': str(e)
        }
        return response_object, False


def get_all_analysis_grids():
    query = AnalysisGrid.query.all()
    analysis_grids = []
    for analysis_grid in query:
        api_response, success = serialize_analysis_grid(analysis_grid)
        if success:
            analysis_grids.append(analysis_grid)
        else:
            return api_response, False
    response_object = {
        'status': 'success',
        'analysis_grids': analysis_grids
    }
    return response_object, True


def get_an_analysis_grid(analysis_grid_id):
    return serialize_analysis_grid(AnalysisGrid.query
                                   .filter_by(id=analysis_grid_id).first())


def serialize_analysis_grid(analysis_grid):
    window_groups = []
    for window_group in analysis_grid.window_groups:
        window_group_data, success = serialize_honeybee_surface(window_group)
        if success:
            window_groups.append(window_group_data['honeybee_surface'])
        else:
            return window_group_data, False

    analysis_grid_json = {
        "id": str(analysis_grid.id),
        "name": str(analysis_grid.name),
        "analysis_points": analysis_grid.analysis_points,
        "window_groups": window_groups
    }

    response_object = {
        'status': 'success',
        'analysis_grid': analysis_grid_json
    }

    return response_object, True


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def grid_point_json(grid_point):
    return {
        "id": str(grid_point.id),
        "x": grid_point.x,
        "y": grid_point.y,
        "z": grid_point.z,
        "vx": grid_point.vx,
        "vy": grid_point.vy,
        "vz": grid_point.vz
    }


def analysis_grid_json(self):
    return {
        "id": str(self.id),
        "name": self.name,
        "analysis_points": [point.to_json() for point in self.analysis_points],
        "window_groups": [window_group.to_json() for
                          window_group in self.window_groups]
    }
