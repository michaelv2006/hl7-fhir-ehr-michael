from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.servicerequest import ServiceRequest
import json

collection = connect_to_mongodb("SamplePatientService", "Procedures")

def GetService_RequestById(Service_request_id: str):
    try:
        Service_request = collection.find_one({"_id": ObjectId(Service_request_id)})
        if Service_request:
            Service_request["_id"] = str(Service_request["_id"])
            return "success", Service_request
        return "notFound", None
    except Exception as e:
        return f"notFound", None

def WriteService_Request(Service_request_dict: dict):
    try:
        req = Service_request.model_validate(Service_request_dict)
    except Exception as e:
        return f"errorValidating: {str(e)}",None
    validated_Service_request_json = req.model_dump()
    result = collection.insert_one(validated_Service_request_json)
    if result:
        inserted_id = str(result.inserted_id)
        return "success",inserted_id
    else:
        return "errorInserting", None

def GetService_RequestByIdentifier(requestSystem,requestValue):
    try:
        Service_request = collection.find_one({"identifier.system":requestSystem,"identifier.value":requestValue})
        if patient:
            Service_request["_id"] = str(Service_request["_id"])
            return "success", Service_request
        return "notFound", None
    except Exception as e:
        return f"error encontrado: {str(e)}", None
