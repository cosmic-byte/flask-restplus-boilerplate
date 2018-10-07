from .. import db
import datetime
import enum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import sqlalchemy


class SurfaceVertices(db.Model):
    __tablename__ = 'surface_vertices'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.String, nullable=False)
    x1 = db.Column(db.Float(), nullable=False)
    y1 = db.Column(db.Float(), nullable=False)
    z1 = db.Column(db.Float(), nullable=False)
    x2 = db.Column(db.Float(), nullable=False)
    y2 = db.Column(db.Float(), nullable=False)
    z2 = db.Column(db.Float(), nullable=False)
    x3 = db.Column(db.Float(), nullable=False)
    y3 = db.Column(db.Float(), nullable=False)
    z3 = db.Column(db.Float(), nullable=False)
    x4 = db.Column(db.Float())
    y4 = db.Column(db.Float())
    z4 = db.Column(db.Float())


class SurfaceTypes(str, enum.Enum):
    wall: str = 'wall'
    underground_wall: str = 'underground wall'
    roof: str = 'roof'
    underground_ceiling: str = 'underground ceiling'
    floor: str = 'floor'
    slab_on_grade: str = 'slab on grade'
    exposed_floor: str = 'exposed floor'
    ceiling: str = 'ceiling'
    window: str = 'window'
    context: str = 'context'


class AnalysisSurface(db.Model):
    __tablename__ = 'analysis_surfaces'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.String, nullable=False)
    vertices_id = db.Column(UUID(as_uuid=True), ForeignKey('surface_vertices.id'), nullable=False)
    name = db.Column(db.String)
    state_name = db.Column(db.String, nullable=False)
    type = db.Column(db.Enum(SurfaceTypes))
    radiance_material_id = db.Column(UUID(as_uuid=True), ForeignKey('materials.id'), nullable=False)

    material = relationship('Material', backref='analysis_surfaces')
    vertices = relationship('SurfaceVertices', backref='analysis_surfaces', lazy="joined")
    # jobs = relationship('Job', secondary='surface_state_groups')


class State(db.Model):
    __tablename__ = 'states'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.Enum(SurfaceTypes))
    radiance_material_id = db.Column(UUID(as_uuid=True), ForeignKey('materials.id'), nullable=False)

    radiance_material = relationship('Material', backref='states')
    honeybee_surfaces = relationship('HoneybeeSurface', secondary='surface_states')


class SurfaceState(db.Model):
    __tablename__ = 'surface_states'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    honeybee_surface_id = db.Column(UUID(as_uuid=True), ForeignKey('honeybee_surfaces.id'), nullable=False)
    state_id = db.Column(UUID(as_uuid=True), ForeignKey('states.id'), nullable=False)

    # honeybee_surface = relationship('HoneybeeSurface', backref='honeybee_surfaces')
    # state = relationship('State', backref='states')


class HoneybeeSurface(db.Model):
    __tablename__ = 'honeybee_surfaces'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.String, nullable=False)

    analysis_surface_id = db.Column(UUID(as_uuid=True), ForeignKey('analysis_surfaces.id'), nullable=False)

    analysis_surface = relationship('AnalysisSurface', backref='honeybee_surface', lazy="joined")
    states = relationship('State', secondary='surface_states')

    # surface_vertices = relationship('SurfaceVertices', secondary='analysis_surfaces')
