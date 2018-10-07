import uuid
import datetime

from app.main import db
from app.main.model.honeybee_surface import SurfaceVertices, AnalysisSurface,\
                                            State, HoneybeeSurface
from app.main.service.material_service import get_a_material
from app.main.service.material_service import save_new_material
from sqlalchemy import and_


def save_new_honeybee_surface(data):
    states = []

    response_object, success = save_new_analysis_surface(data)

    if not success:
        return response_object, 409

    if 'states' in data.keys():
        for state_data in data['states']:
            state_data['user_id'] = data['user_id']
            api_response, success = create_surface_state(state_data,
                                                         data['user_id'])
            if success:
                states.append(api_response['state'])
            else:
                return api_response, 409

    new_honeybee_surface = HoneybeeSurface(
        id=str(uuid.uuid4()),
        created_on=datetime.datetime.utcnow(),
        created_by=str(data['user_id']),
        updated_on=datetime.datetime.utcnow(),
        updated_by=str(data['user_id']),

        analysis_surface_id=response_object['id'],
        states=states
        )

    try:
        save_changes(new_honeybee_surface)
        response_object = {
            'status': 'success',
            'message': 'sucesfully created honeybee surface',
            'id': str(new_honeybee_surface.id)
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'failure',
            'message': 'something went wrong adding new honeybee surface to the database',
            'error': str(e)
        }
        return response_object, 409


def save_new_analysis_surface(data):
    if 'state_name' not in data.keys():
        data['state_name'] = 'default'

    if 'id' in data['radiance_material'].keys():
        radiance_material_id = data['radiance_material']['id']
        if get_a_material(radiance_material_id) is None:
            response_object = {
                'status': 'fail',
                'message': 'material with id {} does not exist'
                .format(radiance_material_id)
            }
            return response_object, False
    else:
        data['radiance_material']['user_id'] = data['user_id']
        api_response, status = save_new_material(data['radiance_material'])
        if 'id' not in api_response.keys():
            return api_response, status
        radiance_material_id = api_response['id']

    response_object, success = save_new_surface_vertices(data)

    if not success:
        return response_object, False

    new_analysis_surface = AnalysisSurface(
        id=str(uuid.uuid4()),
        created_on=datetime.datetime.utcnow(),
        created_by=str(data['user_id']),
        updated_on=datetime.datetime.utcnow(),
        updated_by=str(data['user_id']),

        name=str(data['name']),
        state_name=str(data['state_name']),
        type=str(data['type']),
        radiance_material_id=radiance_material_id,
        vertices_id=response_object['id']
        )
    try:
        save_changes(new_analysis_surface)
        response_object = {
            'status': 'success',
            'message': 'successfully created analysis surface',
            'id': new_analysis_surface.id
        }
        return response_object, True,
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'something went wrong saving analysis surface to the database',
            'error': str(e)
        }
        return response_object, False


def create_surface_state(data, user_id):
    if 'id' in data['radiance_material'].keys():
        radiance_material_id = data['radiance_material']['id']
        if get_a_material(radiance_material_id) is None:
            response_object = {
                'status': 'fail',
                'message': 'material with id {} does not exist'
                .format(radiance_material_id)
            }
            return response_object, False
    else:
        data['radiance_material']['user_id'] = data['user_id']
        api_response, status = save_new_material(data['radiance_material'])
        if 'id' not in api_response.keys():
            return api_response, status
        radiance_material_id = api_response['id']

    state = State.query.filter(and_(State.name == data['name'],
                                    State.type == data['type'],
                                    State.radiance_material_id
                                    == radiance_material_id)).first()
    if not state:
        state = State(
            id=str(uuid.uuid4()),
            created_on=datetime.datetime.utcnow(),
            created_by=user_id,
            updated_on=datetime.datetime.utcnow(),
            updated_by=user_id,
            name=data['name'],
            type=data['type'],
            radiance_material_id=radiance_material_id
        )
    response_object = {
        'status': 'success',
        'message': 'sucessfully found/created state',
        'state': state
    }
    return response_object, True


def save_new_surface_vertices(data):
    vertices = data['vertices']
    if len(vertices) < 3 or len(vertices) > 4:
        response_object = {
            'status': 'fail',
            'message': 'Vertices array expects 3 or 4 vertices, not {}'
            .format(str(len(vertices)))
        }
        return response_object, False
    elif len(vertices) == 4:
        x4 = vertices[3]['x']
        y4 = vertices[3]['y']
        z4 = vertices[3]['z']
    else:
        x4 = None
        y4 = None
        z4 = None

    new_surface_vertices = SurfaceVertices(
        id=str(uuid.uuid4()),
        created_on=datetime.datetime.utcnow(),
        created_by=str(data['user_id']),
        updated_on=datetime.datetime.utcnow(),
        updated_by=str(data['user_id']),
        x1=vertices[0]['x'],
        y1=vertices[0]['y'],
        z1=vertices[0]['z'],
        x2=vertices[1]['x'],
        y2=vertices[1]['y'],
        z2=vertices[1]['z'],
        x3=vertices[2]['x'],
        y3=vertices[2]['y'],
        z3=vertices[2]['z'],
        x4=x4,
        y4=y4,
        z4=z4
    )

    try:
        save_changes(new_surface_vertices)
        response_object = {
            'status': 'success',
            'message': 'Successfully created surface vertices',
            'id': new_surface_vertices.id
        }
        return response_object, True
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Something went wrong when saving vertices to the database',
            'error': str(e)
        }
        return response_object, False


def vertices_to_json(vertices):
    try:
        response_object = {
            'status': 'success',
            'vertices': [
                {
                    'x': vertices.x1,
                    'y': vertices.y1,
                    'z': vertices.z1
                },
                {
                    'x': vertices.x2,
                    'y': vertices.y2,
                    'z': vertices.z2
                },
                {
                    'x': vertices.x3,
                    'y': vertices.y3,
                    'z': vertices.z3
                }
            ]
        }

        if vertices.x4 is not None:
            response_object['vertices'].append(
                {
                    'x': vertices.x4,
                    'y': vertices.y4,
                    'z': vertices.z4
                })

        return response_object, True
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Something went wrong when deserializing surface vertices',
            'error': str(e)
        }

        return response_object, False


def serialize_honeybee_surface(honeybee_surface):
    api_response, success = vertices_to_json(
        honeybee_surface.analysis_surface.vertices)
    if success:
        honeybee_surface_json = {
            'id': honeybee_surface.id,
            'name': honeybee_surface.analysis_surface.name,
            'type': honeybee_surface.analysis_surface.type._value_,
            'state_name': honeybee_surface.analysis_surface.state_name,
            'radiance_material': honeybee_surface.analysis_surface.material,
            'vertices': api_response['vertices'],
            'states': honeybee_surface.states
        }

        response_object = {
            'status': 'success',
            'honeybee_surface': honeybee_surface_json
        }
        return response_object, True
    else:
        return api_response, False


def get_all_honeybee_surfaces():
    query = HoneybeeSurface.query.all()
    honeybee_surfaces = []
    for honeybee_surface in query:
        api_response, success = serialize_honeybee_surface(honeybee_surface)
        if success:
            honeybee_surfaces.append(api_response['honeybee_surface'])
        else:
            return api_response, False
    response_object = {
        'status': 'success',
        'honeybee_surfaces': honeybee_surfaces
    }
    return response_object, True


def get_a_honeybee_surface(honeybee_surface_id):
    return serialize_honeybee_surface(HoneybeeSurface.query.filter_by(id=honeybee_surface_id).first())


def save_changes(data):
    db.session.add(data)
    db.session.commit()
