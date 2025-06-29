#Creacion del modelo de la base de datos.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

#Cargar variables de entorno desde .env
load_dotenv()

#Leer las variables del .env
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

#Creamos URL de conexion.
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#Creamos el engine (motor de conexion)
engine = create_engine(DATABASE_URL)

#Creamos la sesion de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Crear tablas
def create_tables():
    import app.models
    Base.metadata.create_all(bind=engine)