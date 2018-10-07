import uuid
import datetime

from app.main import db
from app.main.model.surface_group import SurfaceGroup
from app.main.model.honeybee_surface import HoneybeeSurface
from app.main.service.honeybee_surface_service import save_new_honeybee_surface,\
                                                      serialize_honeybee_surface


def save_new_surface_group(data):
    honeybee_surface_ids = []

    for honeybee_surface_data in data['honeybee_surfaces']:
        if 'id' not in honeybee_surface_data.keys():
            honeybee_surface_data['user_id'] = data['user_id']
            api_response, status_code =\
                save_new_honeybee_surface(honeybee_surface_data)
            if api_response['status'] != 'success':
                return api_response, 409
            hbs_id = api_response['id']
        else:
            hbs_id = honeybee_surface_data['id']
        honeybee_surface_ids.append(hbs_id)

    honeybee_surfaces = HoneybeeSurface.query.filter(
        HoneybeeSurface.id.in_(honeybee_surface_ids)
        ).all()

    missing_ids = []
    if len(honeybee_surfaces) != len(honeybee_surface_ids):
        query_ids = [hbs.id for hbs in honeybee_surfaces]
        missing_ids = [x for x in query_ids if x not in honeybee_surface_ids]

    new_surface_group = SurfaceGroup(
        id=str(uuid.uuid4()),
        created_on=datetime.datetime.utcnow(),
        created_by=str(data['user_id']),
        updated_on=datetime.datetime.utcnow(),
        updated_by=str(data['user_id']),

        name=data['name'],
        description=data['description'],
        honeybee_surfaces=honeybee_surfaces
    )

    try:
        save_changes(new_surface_group)
        response_object = {
            'status': 'success',
            'id': str(new_surface_group.id),
            'message': 'Successfully created surface group.'
        }
        if len(missing_ids) != 0:
            response_object['missing_ids'] = missing_ids
            response_object['message'] = response_object['message'] + \
                ' Some surface ids provided were not found in the database'
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Something went wrong when creating the surface group',
            'error': str(e)
        }
        return response_object, 409


def serialize_surface_group(data):
    return {
        'id': data.id,
        'name': data.name,
        'description': data.description,
        'honeybee_surface_count': len(data.honeybee_surfaces)
    }


def get_all_surface_groups():
    query = SurfaceGroup.query.all()
    surface_groups = []
    for surface_group in query:
        surface_groups.append(serialize_surface_group(surface_group))
    response_object = {
        'status': 'success',
        'surface_groups': surface_groups
    }
    return response_object, 200


def get_a_surface_group(surface_group_id):
    surface_group = SurfaceGroup.query.filter_by(id=surface_group_id).first()
    try:
        honeybee_surfaces = [serialize_honeybee_surface(hbs) for hbs
                             in surface_group.honeybee_surfaces]
        surface_group = {
            'id': surface_group.id,
            'name': surface_group.name,
            'description': surface_group.description,
            'honeybee_surfaces': honeybee_surfaces,
            'honeybee_surface_count': len(honeybee_surfaces)
        }
        response_object = {
            'status': 'success',
            'surface_group': surface_group
        }
        return response_object, True
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'something went wrong when fetching the surface group',
            'error': str(e)
        }
        return response_object, False


def save_changes(data):
    db.session.add(data)
    db.session.commit()
