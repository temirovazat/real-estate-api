import sqlalchemy

from app.db.metadata import postgres_metadata

unit_amenities = sqlalchemy.Table(
    "unit_amenities",
    postgres_metadata,
    sqlalchemy.Column(
        "amenity_id", sqlalchemy.ForeignKey("amenity.id"), primary_key=True
    ),
    sqlalchemy.Column("unit_id", sqlalchemy.ForeignKey("unit.id"), primary_key=True),
)

# e.g. SPA, gym, pool, golf, tennis, basketball, etc.
amenity = sqlalchemy.Table(
    "amenity",
    postgres_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True, index=True),
)

building = sqlalchemy.Table(
    "building",
    postgres_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("name", sqlalchemy.String, default=""),
    sqlalchemy.Column("description", sqlalchemy.String, default=""),
    sqlalchemy.Column("latitude", sqlalchemy.Numeric, nullable=False),
    sqlalchemy.Column("longitude", sqlalchemy.Numeric, nullable=False),
    sqlalchemy.Column("building_class", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("postcode", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("number_of_units", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("number_of_floors", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("year_built", sqlalchemy.String, nullable=False),
)

unit = sqlalchemy.Table(
    "unit",
    postgres_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("description", sqlalchemy.String, default=""),
    sqlalchemy.Column("price", sqlalchemy.Numeric, nullable=False),
    sqlalchemy.Column("square", sqlalchemy.Numeric, nullable=False),
    sqlalchemy.Column("bedrooms", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("bathrooms", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column(
        "building_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("building.id", ondelete="CASCADE"),
    ),
)
