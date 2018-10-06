from .. import db
import datetime
import enum
from sqlalchemy.dialects.postgresql import JSONB, UUID
import sqlalchemy


class MaterialTypes(str, enum.Enum):
    bsdf: str = 'bsdf'
    light_source: str = 'light_source'
    opaque: str = 'opaque'
    translucent: str = 'translucent'


class Material(db.Model):
    """ Material Model for storing material data """
    __tablename__ = 'materials'

    # id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.String, nullable=False)

    name = db.Column(db.String)
    type = db.Column(db.Enum(MaterialTypes), nullable=False)
    # data = db.Column(JSONB, nullable=False)

    red = db.Column(db.Float)
    green = db.Column(db.Float)
    blue = db.Column(db.Float)
    radius = db.Column(db.Float)
    r_reflectance = db.Column(db.Float)
    g_reflectance = db.Column(db.Float)
    b_reflectance = db.Column(db.Float)
    specularity = db.Column(db.Float)
    roughness = db.Column(db.Float)
    r_transmittance = db.Column(db.Float)
    g_transmittance = db.Column(db.Float)
    b_transmittance = db.Column(db.Float)
    xml_data = db.Column(db.String)
    up_orientation = db.Column(db.Float)
    thickness = db.Column(db.Float)
    refraction = db.Column(db.Float)
    modifier = db.Column(db.String)

    def __repr__(self):
        return "<Material type: {} id: {}>".format(self.type, str(self.id))
