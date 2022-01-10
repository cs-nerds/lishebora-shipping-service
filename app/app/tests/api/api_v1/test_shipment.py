import datetime
import uuid
from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.conf import settings
from app.models.main import Country
from app.tests.utils.location import create_random_location
from app.tests.utils.shipment import create_random_shipment
from app.tests.utils.utils import random_lower_string


def test_create_shipment_ok(client: TestClient, db: Session) -> Any:
    url = f"{settings.API_V1_STR}/shipments/create"

    country = db.query(Country).first()
    from_location = create_random_location(
        name=random_lower_string(), country_uuid=country.uuid, db=db
    )
    to_location = create_random_location(
        name=random_lower_string(), country_uuid=country.uuid, db=db
    )

    shipment_schema = dict(
        sender_user_id=str(uuid.uuid4()),
        receiver_user_id=str(uuid.uuid4()),
        shipping_date=str(datetime.date.today()),
        from_location=str(from_location.uuid),
        to_location=str(to_location.uuid),
        status="pending",
    )

    res = client.post(url, json=shipment_schema)
    res_json = res.json()

    assert res.status_code == 201

    assert res_json.get("status") == "success"
    assert res_json.get("message") is not None
    assert res_json.get("result") is not None
    assert type(res_json.get("result")) == dict
    assert res_json.get("result").get("from_location") == shipment_schema.get(
        "from_location"
    )


def test_update_shipment_ok(client: TestClient, db: Session) -> Any:
    url = f"{settings.API_V1_STR}/shipments/update"

    shipment = create_random_shipment(db=db)

    shipment_schema = dict(
        shipping_date=str(datetime.date.today() + datetime.timedelta(days=1)),
        uuid=str(shipment.uuid),
        status="pending",
        sender_user_id=str(shipment.sender_user_id),
        receiver_user_id=str(shipment.receiver_user_id),
        from_location=str(shipment.from_location),
        to_location=str(shipment.to_location),
    )

    res = client.patch(url, json=shipment_schema)
    res_json = res.json()

    assert res.status_code == 200
    assert res_json.get("status") == "success"
    assert res_json.get("message") is not None
    assert res_json.get("result") is not None
    assert type(res_json.get("result")) == dict
    assert res_json.get("result").get("shipping_date") == shipment_schema.get(
        "shipping_date"
    )


def test_update_shipment_404(client: TestClient, db: Session) -> Any:
    url = f"{settings.API_V1_STR}/shipments/update"

    shipment = create_random_shipment(db=db)

    shipment_schema = dict(
        shipping_date=str(datetime.date.today() + datetime.timedelta(days=1)),
        uuid=str(uuid.uuid4()),
        status="pending",
        sender_user_id=str(shipment.sender_user_id),
        receiver_user_id=str(shipment.receiver_user_id),
        from_location=str(shipment.from_location),
        to_location=str(shipment.to_location),
    )

    res = client.patch(url, json=shipment_schema)
    res_json = res.json()

    assert res.status_code == 404
    assert res_json.get("status") == "error"
    assert res_json.get("error") is not None


def test_get_shipment_details_ok(client: TestClient, db: Session) -> Any:
    url = f"{settings.API_V1_STR}/shipments/details"

    shipment = create_random_shipment(db=db)

    params = {"shipment_uuid": shipment.uuid}

    res = client.get(url, params=params)
    res_json = res.json()

    assert res.status_code == 200
    assert res_json.get("status") == "success"
    assert res_json.get("message") is not None
    assert res_json.get("result") is not None
    assert type(res_json.get("result")) == dict
    assert res_json.get("result").get("uuid") == str(shipment.uuid)


def test_get_shipment_details_404(client: TestClient, db: Session) -> Any:
    url = f"{settings.API_V1_STR}/shipments/details"

    params = {
        "shipment_uuid": uuid.uuid4(),
    }

    res = client.get(url, params=params)
    res_json = res.json()

    assert res.status_code == 404
    assert res_json.get("status") == "error"
    assert res_json.get("error") is not None
