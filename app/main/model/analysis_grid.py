from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import sqlalchemy


class GridPoint(db.Model):
    __tablename__ = 'grid_points'
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.String, nullable=False)

    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    z = db.Column(db.Float, nullable=False)
    vx = db.Column(db.Float, nullable=False)
    vy = db.Column(db.Float, nullable=False)
    vz = db.Column(db.Float, nullable=False)

    analysis_grid = relationship('AnalysisGrid', secondary='analysis_grid_join_point')


class AnalysisGrid(db.Model):
    __tablename__ = 'analysis_grids'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.String, nullable=False)

    name = db.Column(db.String)

    analysis_points = relationship('GridPoint', secondary='analysis_grid_join_point', lazy='joined')
    window_groups = relationship('HoneybeeSurface', secondary='window_groups', lazy='joined')


class AnalysisGridJoinPoint(db.Model):
    __tablename__ = 'analysis_grid_join_point'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    analysis_grid = db.Column(UUID(as_uuid=True), ForeignKey('analysis_grids.id'))
    grid_point = db.Column(UUID(as_uuid=True), ForeignKey('grid_points.id'))


class WindowGroup(db.Model):
    __tablename__ = 'window_groups'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    analysis_grid = db.Column(UUID(as_uuid=True), ForeignKey('analysis_grids.id'))
    honeybee_surface = db.Column(UUID(as_uuid=True), ForeignKey('honeybee_surfaces.id'))
