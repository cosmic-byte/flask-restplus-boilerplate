import uuid
import datetime

from app.main import db
from app.main.model.material import Material


def save_new_material(data):
    material = Material.query.filter_by(name=data['name']).first()

    if not material:
        material_type = data['type']

        new_material = Material(
            id=str(uuid.uuid4()),
            created_on=datetime.datetime.utcnow(),
            created_by=str(data['user_id']),
            updated_on=datetime.datetime.utcnow(),
            updated_by=str(data['user_id']),

            name=str(data['name']),
            type=str(data['type'])
        )
        if material_type == 'bsdf':
            response_object, status_code =\
                check_required_values(data, ['xml_data',
                                             'up_orientation',
                                             'thickness'])
            if response_object:
                return response_object, status_code

            inject_keys_into_dict(new_material,
                                  data,
                                  ['xml_data', 'up_orientation',
                                   'thickness', 'modifier'])

        elif material_type == 'light_source':
            response_object, status_code =\
                check_required_values(data, ['red', 'green', 'blue', 'radius'])
            if response_object:
                return response_object, status_code

            inject_keys_into_dict(new_material,
                                  data,
                                  ['red', 'green', 'blue',
                                   'radius', 'modifier'])

        elif material_type == 'opaque':
            response_object, status_code =\
                check_required_values(data,
                                      ['r_reflectance', 'g_reflectance',
                                       'b_reflectance', 'specularity',
                                       'roughness'])
            if response_object:
                return response_object, status_code

            inject_keys_into_dict(new_material,
                                  data,
                                  ['r_reflectance', 'g_reflectance',
                                   'b_reflectance', 'specularity',
                                   'roughness', 'modifier'])

        elif material_type == 'translucent':
            response_object, status_code =\
                check_required_values(data,
                                      ['r_transmittance', 'g_transmittance',
                                       'b_transmittance', 'refraction'])
            if response_object:
                return response_object, status_code
            inject_keys_into_dict(new_material,
                                  data,
                                  ['r_transmittance', 'g_transmittance',
                                   'b_transmittance', 'refraction',
                                   'modifier'])

        try:
            save_changes(new_material)
            response_object = {
                'status': 'success',
                'message': 'Successfully created object.',
                'id': str(new_material.id)
            }
            return response_object, 201
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'custom error message',
                'errors': str(e)
            }
            return response_object, 409

    else:
        object_id = material.id
        response_object = {
            'status': 'fail',
            'message': 'Material with that name already exists',
            'id': str(object_id)
        }
        return response_object, 409


def get_all_materials():
    return Material.query.all()


def get_a_material(material_id):
    return Material.query.filter_by(id=material_id).first()


def inject_keys_into_dict(new_dict, old_dict, keys):
    for key in keys:
        if key in old_dict.keys():
            setattr(new_dict, key, old_dict[key])


def check_required_values(data, values):
    for value in values:
        if value not in data.keys():
            response_object = {
                'status': 'fail',
                'message': 'Property {} is required for materials of type {}'
                .format(value, data['type'])
            }
            return response_object, 409
    return None, None


def save_changes(data):
    db.session.add(data)
    db.session.commit()
    db.session.flush()
    return data.id
