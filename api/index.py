import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from api.arbol import ArbolTorneo

app = FastAPI(title="Motor de Diagnostico API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

torneo_actual = ArbolTorneo(10)

class ConfigTorneo(BaseModel):
    niveles: int

class NodoRaiz(BaseModel):
    valor: str

class NodoHijo(BaseModel):
    padre: str
    valor: str
    direccion: str

class DatosReconstruccion(BaseModel):
    preorden: list
    inorden: list

def buscar_nodo(nodo_actual, valor_buscado):
    if nodo_actual is None:
        return None
    if nodo_actual.valor == str(valor_buscado):
        return nodo_actual
    
    encontrado_izq = buscar_nodo(nodo_actual.izquierdo, valor_buscado)
    if encontrado_izq: 
        return encontrado_izq
        
    return buscar_nodo(nodo_actual.derecho, valor_buscado)

# ==========================================
# LA MAGIA: PYTHON AHORA MUESTRA EL DISEÑO
# ==========================================
@app.get("/")
def home():
    # Encuentra el index.html sin importar dónde lo ponga Vercel
    ruta_html = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index.html")
    return FileResponse(ruta_html)

@app.post("/iniciar")
def iniciar_torneo(config: ConfigTorneo):
    global torneo_actual
    torneo_actual = ArbolTorneo(config.niveles)
    return {"mensaje": f"Arbol inicializado con {config.niveles} niveles maximos."}

@app.post("/insertar/raiz")
def insertar_raiz(datos: NodoRaiz):
    exito, msj = torneo_actual.insertar_raiz(datos.valor)
    if not exito:
        raise HTTPException(status_code=400, detail=msj)
    return {"mensaje": msj}

@app.post("/insertar/hijo")
def insertar_hijo(datos: NodoHijo):
    padre_obj = buscar_nodo(torneo_actual.raiz, datos.padre)
    if not padre_obj:
        raise HTTPException(status_code=404, detail="Nodo padre no encontrado.")
    
    exito, msj = torneo_actual.insertar_hijo(padre_obj, datos.valor, datos.direccion)
    if not exito:
        raise HTTPException(status_code=400, detail=msj)
        
    return {"mensaje": msj}

@app.get("/recorridos")
def obtener_recorridos():
    if torneo_actual.raiz is None:
        raise HTTPException(status_code=404, detail="El arbol esta vacio.")
        
    return {
        "preorden": torneo_actual.recorrido_preorden(torneo_actual.raiz),
        "inorden": torneo_actual.recorrido_inorden(torneo_actual.raiz),
        "postorden": torneo_actual.recorrido_postorden(torneo_actual.raiz)
    }

@app.get("/estructura")
def obtener_estructura():
    if torneo_actual.raiz is None:
        return None
    return torneo_actual.obtener_estructura(torneo_actual.raiz)

@app.post("/reconstruir")
def reconstruir_arbol(datos: DatosReconstruccion):
    global torneo_actual
    arbol_nuevo = ArbolTorneo(torneo_actual.max_niveles)
    raiz_reconstruida = arbol_nuevo.reconstruir_arbol(datos.preorden, datos.inorden)
    
    if not raiz_reconstruida:
        raise HTTPException(status_code=400, detail="Error: Preorden e Inorden no coinciden.")
        
    arbol_nuevo.raiz = raiz_reconstruida
    torneo_actual = arbol_nuevo
    return torneo_actual.obtener_estructura(torneo_actual.raiz)