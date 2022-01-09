from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.conf import settings
from app.models.main import Country
from app.schemas.locations import CreateLocationSchema, UpdateLocationSchema
from app.tests.utils.utils import random_float, random_lower_string
from app.tests.utils.location import create_random_location
import uuid

def test_create_location_ok(client: TestClient, db: Session) -> Any:
    url = f"{settings.API_V1_STR}/locations/create"
    test_country = db.query(Country).first()
    location_name = random_lower_string()
    payload = CreateLocationSchema(
        name=location_name,
        latitude=random_float(),
        longitude=random_float(),
        country_uuid=test_country.uuid,
    )
    data = payload.dict()
    data["country_uuid"] = str(test_country.uuid)

    res = client.post(url, json=data)

    assert res.status_code == 201
    res_json = res.json()
    assert res_json.get("status") == "success"
    assert res_json.get("message") is not None
    assert type(res_json.get("result")) == dict
    assert res_json.get("result").get("country_uuid") == str(test_country.uuid)
    assert res_json.get("result").get("name") == location_name

def test_list_locations_ok(client: TestClient, db: Session) -> Any:
    url = f"{settings.API_V1_STR}/locations/list"
    test_country = db.query(Country).first()
    params = {'country_uuid': test_country.uuid}
    res = client.get(url, params=params)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json.get("status") == "success"
    assert res_json.get("message") is not None
    assert type(res_json.get("result")) == list


def test_get_location_details_ok(client: TestClient, db: Session) -> Any:
    url = f"{settings.API_V1_STR}/locations/details"
    test_country = db.query(Country).first()
    test_location = create_random_location(
        name=random_lower_string(),
        country_uuid=test_country.uuid,
        db=db,
    )
    params = {'location_uuid': test_location.uuid}
    res = client.get(url, params=params)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json.get("status") == "success"
    assert res_json.get("message") is not None
    assert type(res_json.get("result")) == dict
    assert res_json.get("result").get("name") == test_location.name
    assert res_json.get("result").get("country_uuid") == str(test_location.country_uuid)

def test_get_location_details_404(client: TestClient, db: Session) -> Any:
    url = f"{settings.API_V1_STR}/locations/details"
    
    params = {'location_uuid': uuid.uuid4()}
    res = client.get(url, params=params)

    assert res.status_code == 404
    res_json = res.json()
    assert res_json.get("status") == "error"
    assert res_json.get("error") is not None
    

