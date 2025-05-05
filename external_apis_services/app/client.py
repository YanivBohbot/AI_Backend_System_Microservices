import httpx
import logging

logger = logging.getLogger("log-service")
logging.basicConfig(level=logging.INFO)


class GeoIPClient:
    # BASE_URL = "https://ipapi.co"
    BASE_URL = "https://ipinfo.io"

    async def get_location(self, ip_address: str) -> dict:
        url = f"{self.BASE_URL}/{ip_address}/json/"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                logger.info("call the api")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": f"Failed to fetch location: {str(e)}"}
