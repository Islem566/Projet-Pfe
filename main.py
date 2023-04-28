from fastapi import FastAPI,Request,File,UploadFile,responses,HTTPException
import json
from datetime import datetime, date, timezone
from pymongo import MongoClient
from bson import ObjectId
from typing import List
from pydantic import BaseModel
import requests
import re
import uuid
from fastapi.responses import JSONResponse
import os

# FastAPIinstance
app = FastAPI()
  
#connexion au mongodb 
client = MongoClient('mongodb://localhost:27017/')
db = client["test"]
mycollection = db["mycollection"]
#Route


@app.post("/json/")
async def read_json(msisdn: int , canal: str , Option_Number: int,file: UploadFile = File(...)):  

    if msisdn is None:
        return {"error code": "1", "Error Message": "Not found"}
   
    if len(str(msisdn)) != 8 or not str(msisdn).isdigit(): 
        return {"error code" : "2", "ErrorMessage": "wrong format"}
    if canal is None:
        return {"error code": "3", "Error Message": "Not found"}
   
    if canal not in ["ussd", "web"]:
               return {"Errorcode": "4" , "ErrorMessage": "Canal Not allowed" }
    if Option_Number > 5:
              return { "error code" : "5" ,  "ErrorMessage":  "Number otpion must be < 5 "}
    
    contents = await file.read()
    body = json.loads(contents)
    for d in body:
      if datetime.strptime(d['supervisionExpiryDate'][:-6], '%Y%m%dT%H:%M:%S') < datetime.today():
             return {"expiration date": d['supervisionExpiryDate'], "message": " msisdn expired"}

     # Query database
    service_class_current = body[0]["serviceClassCurrent"]
    result = ";" + service_class_current
    cursor = db.mycollection.find({"serviceClassCurrent": re.compile(result)})
      
    documents = []
    for document in cursor:
        document["_id"] = str(document["_id"]) 
        documents.append(document)
    return JSONResponse(content={"documents": documents})

 


 

                
            
            















