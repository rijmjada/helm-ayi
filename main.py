from fastapi import FastAPI, Request, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = FastAPI()

USER = os.getenv("MYSQL_USER", "root")
PASSWORD = os.getenv("MYSQL_PASSWORD", "admin")
HOST = os.getenv("MYSQL_HOST", "localhost")
PORT = os.getenv("MYSQL_PORT", "3306")
DB = os.getenv("MYSQL_DATABASE", "testdb")
LOG_FILE = os.getenv("LOG_FILE", "/app/data/accesos.log")

# Ensure the log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configure logging
acceso_logger = logging.getLogger("accesos")
handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter("%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
acceso_logger.addHandler(handler)
acceso_logger.setLevel(logging.INFO)

# Also log to console for Kubernetes pod logs
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
acceso_logger.addHandler(console_handler)

DATABASE_URL_NO_DB = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/"
DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def crear_engine_y_session():
    global engine, SessionLocal
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def crear_base_si_no_existe():
    # Intentar crear la base si no existe (solo para POST /crear)
    try:
        # Probar conexión simple
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        acceso_logger.info(f"Conexión exitosa a la base de datos: {DB}")
    except OperationalError as e:
        acceso_logger.warning(f"Error de conexión a {DB}, intentando crear la base de datos: {e}")
        # Conectar sin DB y crearla
        engine_no_db = create_engine(DATABASE_URL_NO_DB, echo=False)
        with engine_no_db.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB}"))
            conn.commit()
        acceso_logger.info(f"Base de datos {DB} creada exitosamente")
        # Crear engine y tablas
        crear_engine_y_session()
        Base.metadata.create_all(bind=engine)
        acceso_logger.info("Tablas creadas exitosamente")

def log_acceso(endpoint: str, request: Request):
    # Handle case where request.client.host can be None
    ip = request.client.host if request.client else "unknown"
    acceso_logger.info(f"Acceso al endpoint {endpoint} desde IP: {ip}")

@app.post("/crear")
async def crear_datos(request: Request):
    log_acceso("/crear", request)
    try:
        crear_base_si_no_existe()
        # Reconectar sesión tras posible recreación
        db = SessionLocal()
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        clientes = [
            Cliente(nombre="Lucía", email="lucia@email.com"),
            Cliente(nombre="Juan", email="juan@email.com"),
            Cliente(nombre="Sofía", email="sofia@email.com"),
        ]
        db.add_all(clientes)
        db.commit()
        db.close()
        acceso_logger.info("Datos creados exitosamente")
        return {"mensaje": "Datos creados"}
    except Exception as e:
        acceso_logger.error(f"Error al crear datos: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

@app.get("/clientes")
async def obtener_clientes(request: Request):
    log_acceso("/clientes", request)
    try:
        db = SessionLocal()
        clientes = db.query(Cliente).all()
        db.close()
        acceso_logger.info(f"Obtenidos {len(clientes)} clientes")
        return [{"id": c.id, "nombre": c.nombre, "email": c.email} for c in clientes]
    except OperationalError as e:
        acceso_logger.error(f"Error de conexión a la base de datos: {e}")
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {e}")
    except Exception as e:
        acceso_logger.error(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

