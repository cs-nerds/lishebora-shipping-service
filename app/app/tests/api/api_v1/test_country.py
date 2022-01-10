import uuid
from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.conf import settings
from app.models.main import Country


def test_get_country_list_ok(client: TestClient, db: Session) -> Any:
    url = f"{settings.API_V1_STR}/countries/list"

    res = client.get(url)
    res_json = res.json()

    assert res.status_code == 200
    assert res_json.get("status") == "success"
    assert type(res_json.get("result")) == list
    assert res_json.get("message") is not None


def test_get_country_details_ok(client: TestClient, db: Session) -> Any:
    url = f"{settings.API_V1_STR}/countries/details"

    country = db.query(Country).first()
    params = {"country_uuid": country.uuid}

    res = client.get(url, params=params)
    res_json = res.json()

    assert res.status_code == 200
    assert res_json.get("status") == "success"
    assert type(res_json.get("result")) == dict
    assert res_json.get("message") is not None
    assert res_json.get("result").get("name") == country.name


def test_get_country_details_404(client: TestClient, db: Session) -> Any:
    url = f"{settings.API_V1_STR}/countries/details"

    params = {"country_uuid": uuid.uuid4()}

    res = client.get(url, params=params)
    res_json = res.json()

    assert res.status_code == 404
    assert res_json.get("status") == "error"
    assert res_json.get("error") is not None
