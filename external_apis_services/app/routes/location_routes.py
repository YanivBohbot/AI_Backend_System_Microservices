from fastapi import APIRouter, HTTPException
from ..client import GeoIPClient

router = APIRouter(prefix="/geoip")

geo_client = GeoIPClient()


@router.get("/{ip}")
async def get_ip_location(ip: str):
    try:
        return await geo_client.get_location(ip)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
