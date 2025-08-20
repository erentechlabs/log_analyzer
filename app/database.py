from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Database URL
# For SQLite, this will create a file named sql_app.db in the project root.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# If you want to switch to PostgreSQL, you can use this line:
# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/database_name"

# 2. Create the SQLAlchemy engine
# connect_args is required only for SQLite. This setting allows multiple threads
# to use the same connection, which is important.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a base class (Base) that our models will inherit from
# All models in models.py will inherit from this Base class.
Base = declarative_base()