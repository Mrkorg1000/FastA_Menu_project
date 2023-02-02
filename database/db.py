from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_NAME, DB_PASS, DB_USER, DB_PORT

# create engine for interaction with database
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)

# create session for the interaction with database
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_session():  # get_db
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()