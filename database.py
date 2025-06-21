from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.recordatorio import Recordatorio
from models.base import Base



# Importa todos los modelos para que se registren en el metadata
from models.usuario import Usuario
from models.tarea import Tarea
# Si tienes más modelos, impórtalos aquí

# Configuración de conexión a la base de datos
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Creador de sesiones
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def crear_bd_y_tablas() -> None:
    """
    Crea la base de datos y sus tablas usando SQLAlchemy ORM.
    """
    Base.metadata.create_all(bind=engine)

def crear_sesion():
    """
    Retorna una nueva sesión de base de datos.
    """
    return SessionLocal()
