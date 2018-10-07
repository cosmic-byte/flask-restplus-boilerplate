import uuid
import datetime

from app.main import db
from app.main.model.epw import EPW, EPWData
from sqlalchemy import and_


def save_new_epw(data):
    time_indexed_data = {}
    timestamp_string_pattern = "%Y-%m-%d %H:%M"
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


def epw_data_row(data, dt):
    data_row = EPWData(datetime=datetime.datetime
                       .strptime(dt, "%Y-%m-%d %H:%M"))

    for key, value in data.items():
        try:
            setattr(data_row, key, value)
        except Exception as e:
            print(e)
    return data_row


def parse_lb_datetime(lb_datetime):
    return datetime.datetime(year=lb_datetime['year'],
                             month=lb_datetime['month'],
                             day=lb_datetime['day'],
                             hour=lb_datetime['hour'],
                             minute=lb_datetime['minute'])


def serialize_lb_datetime(dt):
    year = dt.year
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                leap_year = True
            else:
                leap_year = False
        else:
            leap_year = True
    else:
        leap_year = False

    return {
        'year': year,
        'month': dt.month,
        'day': dt.day,
        'hour': dt.hour,
        'minute': dt.minute,
        'leap_year': leap_year
    }


def serialize_epw(epw):
    data_collections = []
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
    for key, value in data_collection_dict.items():
        data_type = ' '.join([name.capitalize() for name in key.split('_')])
        data_collections.append({
            'header': {
                'data_type': data_type
            },
            'data': value
        })

    epw_json = {
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
        },
        'data': data_collections
    }
    return epw_json


def get_all_epws():
    query = EPW.query.filter_by(is_wea=False).all()  # .noload()
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


def get_an_epw(epw_id):
    return serialize_epw(EPW.query.filter_by(id=epw_id).first())


def save_changes(data):
    db.session.add(data)
    db.session.commit()
