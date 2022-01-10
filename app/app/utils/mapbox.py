from typing import Any

from mapbox import Directions, Geocoder

from app.core.conf import settings


def mapbox_geocoding(
    location_name: str, country: str = "Ke", language: str = "en"
) -> Any:
    geocoder = Geocoder(access_token=settings.MAPBOX_ACCESS_TOKEN)
    response = geocoder.forward(
        address=location_name, country=country, languages=language
    )
    return response


def mapbox_get_distance_km(point1: tuple, point2: tuple) -> float:
    service = Directions(access_token=settings.MAPBOX_ACCESS_TOKEN)
    origin = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": list(point1)},
    }
    destination = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": list(point2)},
    }
    features = [origin, destination]
    response = service.directions(features=features, profile="mapbox.driving")
    driving_routes = response.geojson()
    driving_properties = driving_routes.get("features")[0].get("properties")
    return driving_properties.get("distance") / 1000
