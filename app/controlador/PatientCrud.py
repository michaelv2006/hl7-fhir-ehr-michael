from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.patient import Patient
from fhir.resources.servicerequest import ServiceRequest
from fhir.resources.procedure import Procedure
import json

collection = connect_to_mongodb("SamplePatientService", "patients")
service_requests_collection = connect_to_mongodb("SamplePatientService", "service_requests")
appointments_collection = connect_to_mongodb("SamplePatientService", "appointments")
procedures_collection = connect_to_mongodb("SamplePatientService", "procedures")

def GetPatientById(patient_id: str):
    try:
        patient = collection.find_one({"_id": ObjectId(patient_id)})
        if patient:
            patient["_id"] = str(patient["_id"])
            return "success", patient
        return "notFound", None
    except Exception as e:
        return f"notFound", None

def WritePatient(patient_dict: dict):
    try:
        pat = Patient.model_validate(patient_dict)
    except Exception as e:
        return f"errorValidating: {str(e)}",None
    validated_patient_json = pat.model_dump()
    result = collection.insert_one(patient_dict)
    if result:
        inserted_id = str(result.inserted_id)
        return "success",inserted_id
    else:
        return "errorInserting", None

def GetPatientByIdentifier(patientSystem,patientValue):
    try:
        patient=collection.find_one({"identifier.system":patientSystem,"identifier.value":patientValue})
        print("patient retornado:",patient)
        if patient:
            patient["_id"]=str(patient["_id"])
            return "success",patient
        return "notFound",None
    except Exception as e:
        return f"error encontrado: {str(e)}",None

def read_service_request(service_request_id: str) -> dict:
    """
    Recupera una solicitud de servicio a partir de su ID.
    """
    try:
        query = {"_id": ObjectId(service_request_id)}
    except Exception as e:
        print("Error al convertir el ID:", e)
        return None

    service_request = service_requests_collection.find_one(query)
    if service_request:
        service_request["_id"] = str(service_request["_id"])
        return service_request
    else:
        return None

def WriteServiceRequest(service_request_dict: dict):
    try:
        sr = ServiceRequest.parse_obj(service_request_dict)
    except Exception as e:
        return f"errorValidating: {str(e)}", None

    # Revisión paso a paso
    subject = service_request_dict.get("subject", {})
    subject_ref = subject.get("reference")

    code = service_request_dict.get("code", {})
    coding_list = code.get("coding", [])
    procedure_code = coding_list[0].get("code") if coding_list else None

    # Imprimir para debug
    print("✅ subject.reference:", subject_ref)
    print("✅ code.coding[0].code:", procedure_code)

    if not subject_ref or not procedure_code:
        return "missingKeyFields", None

    # Verificar si ya existe
    existing = service_requests_collection.find_one({
        "subject.reference": subject_ref,
        "code.coding.0.code": procedure_code
    })

    if existing:
        return "alreadyExists", str(existing["_id"])

    # Insertar si no existe
    result = service_requests_collection.insert_one(service_request_dict)
    if result.inserted_id:
        return "success", str(result.inserted_id)
    else:
        return "errorInserting", None


def read_appointment(appointment_id: str) -> dict:
    """
    Recupera un Appointment a partir de su ID.
    """
    try:
        query = {"_id": ObjectId(appointment_id)}
    except Exception as e:
        print("Error al convertir el ID:", e)
        return None

    appointment = appointments_collection.find_one(query)
    if appointment:
        appointment["_id"] = str(appointment["_id"])
        return appointment
    else:
        return None

def WriteAppointment(appointment_data: dict):
    """
    Inserta un Appointment en la base de datos si existe la ServiceRequest asociada
    y no ha sido usada ya para otra cita.
    """
    try:
        based_on_list = appointment_data.get("basedOn", [])
        if not based_on_list:
            return "missingServiceRequestReference", None

        sr_ref = based_on_list[0].get("reference")  # "ServiceRequest/682e57308763ad8542ed578d"
        if not sr_ref or not sr_ref.startswith("ServiceRequest/"):
            return "invalidServiceRequestReference", None

        sr_id = sr_ref.split("/")[1]

        try:
            sr_oid = ObjectId(sr_id)
        except Exception:
            return "invalidObjectId", None

        # Verificar si el ServiceRequest existe
        sr = service_requests_collection.find_one({"_id": sr_oid})
        if not sr:
            return "serviceRequestNotFound", None

        # Verificar si ya hay un Appointment asociado a este ServiceRequest
        existing_appt = appointments_collection.find_one({
            "basedOn.reference": sr_ref
        })

        if existing_appt:
            return "appointmentAlreadyExists", None

        # Si no existe, se inserta
        result = appointments_collection.insert_one(appointment_data)
        return "success", str(result.inserted_id)

    except Exception as e:
        print("Error en WriteAppointment:", e)
        return "error", None

def WriteProcedure(procedure_data: dict):
    try:
        based_on_list = procedure_data.get("basedOn", [])
        if not based_on_list:
            return "missingServiceRequestReference", None

        sr_ref = based_on_list[0].get("reference")  # e.g. "ServiceRequest/682e..."
        if not sr_ref or not sr_ref.startswith("ServiceRequest/"):
            return "invalidServiceRequestReference", None

        sr_id = sr_ref.split("/")[1]
        try:
            sr_oid = ObjectId(sr_id)
        except Exception:
            return "invalidObjectId", None

        sr = service_requests_collection.find_one({"_id": sr_oid})
        if not sr:
            return "serviceRequestNotFound", None

        result = procedures_collection.insert_one(procedure_data)
        return "success", str(result.inserted_id)

    except Exception as e:
        print("Error en WriteProcedure:", e)
        return "error", None

def read_procedure(procedure_id: str) -> dict:
    """
    Recupera un Procedure a partir de su ID.
    """
    try:
        query = {"_id": ObjectId(procedure_id)}
    except Exception as e:
        print("Error al convertir el ID:", e)
        return None

    procedure = procedures_collection.find_one(query)
    if procedure:
        procedure["_id"] = str(procedure["_id"])
        return procedure
    else:
        return None
