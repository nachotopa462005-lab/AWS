import os
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime
from dotenv import load_dotenv

# 1. Cargar variables del .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Configurar Base de Datos AWS RDS
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Modelos de las Tablas (Consigna)
class Inventario(Base):
    __tablename__ = "inventario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    cantidad = Column(Integer)
    precio = Column(Float)

class LogIP(Base):
    __tablename__ = "logs_ips"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=True)
    fecha_acceso = Column(DateTime, default=datetime.utcnow)

# Crear tablas automáticamente en RDS si no existen
Base.metadata.create_all(bind=engine)

# 4. Inicializar Aplicación
app = FastAPI(title="Stack ASIR con AWS RDS")

# Dependencia para sesiones de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 5. Endpoints GET (Lectura)
@app.get("/")
def inicio():
    return {"status": "ok", "mensaje": "FastAPI conectado exitosamente a AWS RDS"}

@app.get("/inventario")
def listar_inventario(db: Session = Depends(get_db)):
    return db.query(Inventario).all()

@app.get("/logs")
def listar_logs(db: Session = Depends(get_db)):
    return db.query(LogIP).all()

# 6. Endpoints POST (Escritura)
@app.post("/inventario")
def crear_item(nombre: str, cantidad: int, precio: float, db: Session = Depends(get_db)):
    nuevo_item = Inventario(nombre=nombre, cantidad=cantidad, precio=precio)
    db.add(nuevo_item)
    db.commit()
    db.refresh(nuevo_item)
    return nuevo_item

@app.post("/logs")
def registrar_log(ip: str, db: Session = Depends(get_db)):
    nuevo_log = LogIP(ip=ip)
    db.add(nuevo_log)
    db.commit()
    db.refresh(nuevo_log)
    return nuevo_log