from .. import db
import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import sqlalchemy


class EPW(db.Model):
    __tablename__ = 'epws'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.String, nullable=False)

    city = db.Column(db.String)
    country = db.Column(db.String)
    source = db.Column(db.String, nullable=False)
    station_id = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float(precision=2), nullable=False)
    longitude = db.Column(db.Float(precision=2), nullable=False)
    time_zone = db.Column(db.Float)
    elevation = db.Column(db.Float(precision=2), nullable=False)

    # wea = relationship('WEA', backref=backref('epw', uselist=False))
    data_points = relationship('EPWData', backref='epw')


class EPWData(db.Model):

    __tablename__ = 'epw_data'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    epw_id = db.Column(UUID(as_uuid=True), ForeignKey('epws.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    years = db.Column(db.Integer)
    dry_bulb_temperature = db.Column(db.Float(precision=2))
    dew_point_temperature = db.Column(db.Float(precision=2))
    relative_humidity = db.Column(db.Float(precision=2))
    atmospheric_station_pressure = db.Column(db.Float(precision=2))
    extraterrestrial_horizontal_radiation = db.Column(db.Float(precision=2))
    extraterrestrial_direct_normal_radiation = db.Column(db.Float(precision=2))
    horizontal_infrared_radiation_intensity = db.Column(db.Float(precision=2))
    global_horizontal_radiation = db.Column(db.Float(precision=2))
    direct_normal_radiation = db.Column(db.Float(precision=2))
    diffuse_horizontal_radiation = db.Column(db.Float(precision=2))
    global_horizontal_illuminance = db.Column(db.Float(precision=2))
    direct_normal_illuminance = db.Column(db.Float(precision=2))
    diffuse_horizontal_illuminance = db.Column(db.Float(precision=2))
    zenith_luminance = db.Column(db.Float(precision=2))
    wind_direction = db.Column(db.Float(precision=2))
    wind_speed = db.Column(db.Float(precision=2))
    total_sky_cover = db.Column(db.Float(precision=2))
    opaque_sky_cover = db.Column(db.Float(precision=2))
    visibility = db.Column(db.Float(precision=2))
    ceiling_height = db.Column(db.Float(precision=2))
    present_weather_observation = db.Column(db.Float(precision=2))
    present_weather_codes = db.Column(db.Float(precision=2))
    precipitable_water = db.Column(db.Float(precision=2))
    aerosol_optical_depth = db.Column(db.Float(precision=2))
    snow_depth = db.Column(db.Float(precision=2))
    days_since_last_snowfall = db.Column(db.Float(precision=2))
    albedo = db.Column(db.Float(precision=2))
    liquid_precipitation_depth = db.Column(db.Float(precision=2))
    liquid_precipitation_quantity = db.Column(db.Float(precision=2))
