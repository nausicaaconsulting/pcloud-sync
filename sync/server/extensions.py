import os

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import MetaData


# Define naming convention for constraints to be able to deal with alter tables
# see https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(
    metadata=metadata,
    engine_options={
        # Test that the database connection is still available at the start of each connection pool checkout
        # see https://docs.sqlalchemy.org/en/14/core/pooling.html#dealing-with-disconnects
        "pool_pre_ping": True,
        "pool_recycle": 1200,  # 20 minutes
    }
)

migrate = Migrate(
    # If True, nest each migration script in a transaction rather than the full series of migrations to run
    transaction_per_migration=True,
    directory=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'migrations'),
)
