from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import RedirectResponse
import models
from database import SessionLocal, engine
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
from middleware import AudiMiddleware

app = FastAPI()
app.add_middleware(AudiMiddleware)



models.Base.metadata.create_all(bind=engine)

class RutaB(BaseModel):
    id_rutas: int
    code: str
    origen: str
    destino: str
    lv: str
    festivos: str
    total_paradas: int
    tiempo_espera: str
    fecha_publicacion: date
    fecha_actualizacion: date
    activo: int

    class Config:
        orm_mode = True


class RutasCenefas(BaseModel):
    id_rutas_cenefas: int
    id_cenefas: int
    id_rutas: int
    code: str
    orden: str
    cenefa: str
    tipo: str
    modulo: str
    cantidad_mm: str
    estado_del_multiple: str
    nombre: str
    direccion_bandera: str
    localidad: str
    consola: str
    panel: str
    audio: str
    longitud: float
    latitud: float
    zona: str
    
    class Config:
        orm_mode = True


class CenefaB(BaseModel):
    id_cenefas: int
    orden: str
    cenefa: str
    tipo: str
    modulo: str
    cantidad_mm: str
    estado_del_multiple: str
    nombre: str
    direccion_bandera: str
    localidad: str
    consola: str
    panel: str
    audio: str
    longitud: float
    latitud: float
    zona: str

    class Config:
        orm_mode = True


origins = [
    "http://localhost",
    "http://127.0.0.1",
    "https://odt.gov.co"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal() 
    try:
        yield db  
    finally:
        db.close() 


@app.get('/')
def main():
    return RedirectResponse(url="/docs/")


@app.get("/all_rutas", response_model=List[RutaB])
def all_rutas(db: Session = Depends(get_db)):
    try:
        db_rutas = db.query(models.Rutas).all()
        if not db_rutas:
            raise HTTPException(status_code=404, detail="No se encontraron rutas")
        
        return db_rutas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ha ocurrido un error: {str(e)}")

@app.get("/ruta/{code}", response_model=List[RutaB])
def all_rutas(code:str, db: Session = Depends(get_db)):
    try:
        db_ruta = db.query(models.Rutas).filter(models.Rutas.code == code)
        if not db_ruta:
            raise HTTPException(status_code=404, detail="No se encontraron rutas")
        
        return db_ruta
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ha ocurrido un error: {str(e)}")



@app.get("/cenefas/{code}", response_model=List[RutasCenefas])
def cenefas(code: str, db: Session = Depends(get_db)):
    try:
        query = db.query(
                    models.RutasCenefas.id.label('id_rutas_cenefas'),
                    models.Rutas.id_rutas.label('id_rutas'),
                    models.Cenefas.id_cenefas.label('id_cenefas'),
                    models.Rutas.code.label('code'),
                    models.Cenefas.orden.label('orden'),
                    models.Cenefas.cenefa.label('cenefa'),
                    models.Cenefas.tipo.label('tipo'),
                    models.Cenefas.modulo.label('modulo'),
                    models.Cenefas.cantidad_mm.label('cantidad_mm'),
                    models.Cenefas.estado_del_multiple.label('estado_del_multiple'),
                    models.Cenefas.nombre.label('nombre'),
                    models.Cenefas.direccion_bandera.label('direccion_bandera'),
                    models.Cenefas.localidad.label('localidad'),
                    models.Cenefas.consola.label('consola'),
                    models.Cenefas.panel.label('panel'),
                    models.Cenefas.audio.label('audio'),
                    models.Cenefas.longitud.label('longitud'),
                    models.Cenefas.latitud.label('latitud'),
                    models.Cenefas.zona.label('zona')
                )\
                .join(models.Rutas, models.RutasCenefas.id_rutas == models.Rutas.id_rutas)\
                .join(models.Cenefas, models.RutasCenefas.id_cenefas == models.Cenefas.id_cenefas)\
                .filter(models.Rutas.code == code)\
                .all()

        if not query:
            raise HTTPException(status_code=404, detail="No se encontraron cenefas con el código especificado")

        return query
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ha ocurrido un error: {str(e)}")