from fastapi import FastAPI, HTTPException,Query
from db import connect_to_mongo, db
from utils import reverse_geocode
from pydantic import BaseModel, Field
from typing import Dict, Optional
# from fastapi import APIRouter,
from bson.objectid import ObjectId

app = FastAPI()

@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()


class LocationModel(BaseModel):
    name: str
    long: float
    lat: float
    org: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/locations")
async def create_location(location: LocationModel):
    address = await reverse_geocode(location.lat, location.long)
    location_doc = {
        "name": location.name,
        "org": location.org,
        "address": address,
        "coordinates": {
            "type": "Point",
            "coordinates": [location.long, location.lat]
        }
    }
    result = await db.locations.insert_one(location_doc)
    return {"id": str(result.inserted_id), "message": "Location added successfully."}

@app.get("/locations")
async def get_locations(
    lat: float = Query(...),
    lng: float = Query(...),
    max_distance: Optional[int] = 1000  # meters
):
    query = {
        "coordinates": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat]
                },
                "$maxDistance": max_distance
            }
        }
    }

    locations = []
    cursor = db.locations.find(query)
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        locations.append(doc)

    return locations