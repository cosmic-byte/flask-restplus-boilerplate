from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy

class SurfaceGroup(db.Model):
    __tablename__ = 'surface_groups'
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.String, nullable=False)

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    honeybee_surfaces = relationship('HoneybeeSurface', secondary='surface_groups_join_honeybee_surfaces')


class SurfaceGroupsJoinHoneybeeSurfaces(db.Model):
    __tablename__ = 'surface_groups_join_honeybee_surfaces'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    surface_group = db.Column(UUID(as_uuid=True), ForeignKey('surface_groups.id'))
    honeybee_surface = db.Column(UUID(as_uuid=True), ForeignKey('honeybee_surfaces.id'))
