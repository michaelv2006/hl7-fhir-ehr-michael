from fastapi import FastAPI, HTTPException, Request
import uvicorn
from app.controlador.PatientCrud import GetPatientById,WritePatient,GetPatientByIdentifier,read_service_request,WriteServiceRequest,read_appointment,WriteAppointment,WriteProcedure,read_procedure
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://write-service-request-mlbj.onrender.com",
    "https://appointment-sjzy.onrender.com",
    "https://procedures.onrender.com"
],
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/patient/{patient_id}", response_model=dict)
async def get_patient_by_id(patient_id: str):
    status,patient = GetPatientById(patient_id)
    if status=='success':
        return patient  # Return patient
    elif status=='notFound':
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")

@app.get("/patient", response_model=dict)
async def get_patient_by_identifier(system: str, value: str):
    print("solicitud datos:",system,value)
    status,patient = GetPatientByIdentifier(system,value)
    if status=='success':
        return patient  # Return patient
    elif status=='notFound':
        raise HTTPException(status_code=204, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")

@app.get("/service-request/{service_request_id}", response_model=dict)
async def get_service_request(service_request_id: str):
    # Llama a la función auxiliar que obtiene la solicitud de servicio
    service_request = read_service_request(service_request_id)
    if service_request:
        return service_request
    else:
        raise HTTPException(status_code=404, detail="Solicitud de servicio no encontrada")

@app.post("/service-request", response_model=dict)
async def add_service_request(request: Request):
    # Obtiene el JSON enviado en la solicitud POST
    service_request_data = await request.json()
    
    # Llama a la función que inserta la solicitud en la base de datos
    status, service_request_id = WriteServiceRequest(service_request_data)
    
    if status == "success":
        return {"_id": service_request_id}
    else:
        raise HTTPException(status_code=500, detail=f"Error al registrar la solicitud: {status}")

@app.get("/appointment/{appointment_id}", response_model=dict)
async def get_appointment(appointment_id: str):
    appointment = read_appointment(appointment_id)
    if appointment:
        return appointment
    else:
        raise HTTPException(status_code=404, detail="Appointment no encontrado")

@app.post("/appointment", response_model=dict)
async def add_appointment(request: Request):
    appointment_data = await request.json()
    status, appointment_id = WriteAppointment(appointment_data)

    if status == "success":
        return {"_id": appointment_id}
    else:
        raise HTTPException(status_code=500, detail=f"Error al registrar el Appointment: {status}")

@app.get("/procedures/{procedure_id}")
def get_procedure(procedure_id: str):
    result = read_procedure(procedure_id)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Procedure no encontrado")

@app.post("/procedures", response_model=dict)
async def add_procedure(request: Request):
    procedure_data = await request.json()
    status, procedure_id = WriteProcedure(procedure_data)

    if status == "success":
        return {"_id": procedure_id}
    elif status == "missingServiceRequestReference":
        raise HTTPException(status_code=400, detail="Falta la referencia a ServiceRequest")
    elif status == "invalidServiceRequestReference":
        raise HTTPException(status_code=400, detail="Referencia de ServiceRequest no válida")
    elif status == "invalidObjectId":
        raise HTTPException(status_code=400, detail="El ID de ServiceRequest no es válido")
    elif status == "serviceRequestNotFound":
        raise HTTPException(status_code=404, detail="ServiceRequest no encontrado")
    else:
        raise HTTPException(status_code=500, detail=f"Error al registrar el Procedure: {status}")

        
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
