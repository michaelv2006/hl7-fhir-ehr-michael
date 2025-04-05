from fastapi import FastAPI, HTTPException, Request
import uvicorn
from app.controlador.ServiceRequestcrud import GetService_RequestById,WriteService_Request,GetService_RequestByIdentifier
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://medservice-94k9.onrender.com", "https://hl7-fhir-ehr-michael.onrender.com"],  # Permitir solo este dominio
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/servicerequest/{Service_Request_id}", response_model=dict)
async def get_Service_request_by_id(Service_request_id: str):
    status, service_request = GetService_RequestById(Service_request_id)  # Llamar a la función que obtiene la solicitud
    if status == 'success':
        return service_request  # Devolver la solicitud si se encuentra
    elif status == 'notFound':
        raise HTTPException(status_code=404, detail="La solicitud de servicio no existe")  # Código 204 si no se encuentra
    else:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor. {status}")  # Error interno

# Ruta para agregar una nueva solicitud de servicio
@app.post("/servicerequest", response_model=dict)
async def add_service_request(request: Request):
    new_service_request_dict = dict(await request.json())  # Convertir la solicitud JSON a un diccionario
    status, request_id = WriteService_Request(new_service_request_dict)  # Llamar a la función que escribe la solicitud
    if status == 'success':
        return {"_id": request_id}  # Devolver el ID de la solicitud si se creó correctamente
    else:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {status}")  # Error interno

# Ruta para obtener una solicitud de servicio por su identificador
@app.get("/servicerequest", response_model=dict)
async def get_service_request_by_identifier(system: str, value: str):
    status, service_request = GetService_RequestByIdentifier(system, value)  # Llamar a la función que busca la solicitud
    if status == 'success':
        return service_request  # Devolver la solicitud si se encuentra
    elif status == 'notFound':
        raise HTTPException(status_code=404, detail="La solicitud de servicio no existe")  # Código 204 si no se encuentra
    else:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor. {status}")  # Error interno
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
