import sqlalchemy

from app.db.metadata import postgres_metadata

developer = sqlalchemy.Table(
    "developer",
    postgres_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column(
        "international_name", sqlalchemy.String, nullable=False, unique=True, index=True
    ),
    sqlalchemy.Column("website", sqlalchemy.String, default=""),
    sqlalchemy.Column("phone_number", sqlalchemy.String, default=""),
)

agent = sqlalchemy.Table(
    "agent",
    postgres_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column(
        "developer_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("developer.id", ondelete="CASCADE"),
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
    ),
)
