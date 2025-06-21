# tests/conftest.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from database import crear_bd_y_tablas
from database import SessionLocal

@pytest.fixture(scope="function")
def db_session():
    """
    Crea una base de datos en memoria para pruebas y devuelve una sesión SQLAlchemy.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
