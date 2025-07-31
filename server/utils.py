import httpx

async def reverse_geocode(lat: float, lng: float) -> str:
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lng,
        "format": "json"
    }
    headers = {"User-Agent": "fastapi-reverse-geocoder (prahlad@example.com)"}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, headers=headers)
        data = resp.json()
        return data.get("display_name", "Unknown address")
