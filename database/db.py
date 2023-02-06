from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

# create engine for interaction with database
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# create session for the interaction with database
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_session():  # get_db
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()