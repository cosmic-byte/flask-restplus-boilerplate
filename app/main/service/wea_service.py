import uuid
import datetime

from app.main import db
from app.main.model.epw import EPW
from app.main.service.epw_service import epw_data_row, serialize_lb_datetime,\
    parse_lb_datetime
from sqlalchemy import and_


def save_new_wea(data):
    time_indexed_data = {}
    timestamp_string_pattern = "%Y-%m-%d %H:%M"
    data['data'] = [data['direct_normal_radiation'],
                    data['diffuse_horizontal_radiation']]
    for data_collection in data['data']:
        col_name = '_'.join(data_collection['header']['data_type'].lower()
                                                                  .split(' '))
        for data_point in data_collection['data']:
            timestamp = parse_lb_datetime(data_point['datetime'])
            timestamp_string = timestamp.strftime(timestamp_string_pattern)
            if timestamp_string not in time_indexed_data.keys():
                time_indexed_data[timestamp_string] = {}
            time_indexed_data[timestamp_string][col_name] = data_point['value']

    data_points = []

    for timestamp, row in time_indexed_data.items():
        data_points.append(epw_data_row(row, timestamp))

    new_epw = EPW(
        id=str(uuid.uuid4()),
        created_on=datetime.datetime.utcnow(),
        created_by=str(data['user_id']),
        updated_on=datetime.datetime.utcnow(),
        updated_by=str(data['user_id']),

        is_wea=True,
        city=data['location']['city'],
        country=data['location']['country'],
        source=data['location']['source'],
        station_id=data['location']['station_id'],
        latitude=data['location']['latitude'],
        longitude=data['location']['longitude'],
        time_zone=data['location']['time_zone'],
        elevation=data['location']['elevation'],
        data_points=data_points
    )

    try:
        save_changes(new_epw)
        response_object = {
            'status': 'success',
            'message': 'successfully created epw',
            'id': str(new_epw.id)
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'something went wrong adding new epw to the database',
            'error': str(e)
        }
        return response_object, 409


def serialize_wea(epw):
    data_collection_dict = {}
    i = 0
    for row in epw.data_points:
        dt = row.datetime
        lb_dt = serialize_lb_datetime(dt)

        for key, item in row.__dict__.items():
            if key not in ['datetime', 'id', 'epw_id', '_sa_instance_state']:
                if key not in data_collection_dict.keys():
                    data_collection_dict[key] = []
                data_point = {
                    'nickname': None,
                    'standard': 'SI',
                    'value': item,
                    'datetime': lb_dt
                }
                data_collection_dict[key].append(data_point)
        i += 1

    wea_json = {
        'id': epw.id,
        'location': {
            'city': epw.city,
            'country': epw.country,
            'source': epw.source,
            'station_id': epw.station_id,
            'latitude': epw.latitude,
            'longitude': epw.longitude,
            'time_zone': epw.time_zone,
            'elevation': epw.elevation
        }
    }

    for key, value in data_collection_dict.items():
        if key in ['direct_normal_radiation', 'diffuse_horizontal_radiation']:
            data_type = ' '.join([name.capitalize() for name in key.split('_')])
            wea_json[key] = {
                'header': {
                    'data_type': data_type
                },
                'data': value
            }

    return wea_json


def get_all_weas():
    query = EPW.query.all()  # .noload()
    epws = []
    for epw in query:
        epws.append({
            'id': epw.id,
            'location': {
                'city': epw.city,
                'country': epw.country,
                'source': epw.source,
                'station_id': epw.station_id,
                'latitude': epw.latitude,
                'longitude': epw.longitude,
                'time_zone': epw.time_zone,
                'elevation': epw.elevation
            }
        })
    return epws


def get_a_wea(epw_id):
    return serialize_wea(EPW.query.filter_by(id=epw_id).first())


def save_changes(data):
    db.session.add(data)
    db.session.commit()
