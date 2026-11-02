import pytest

def loan_payload(
        id=1,
        equipment_id = 2,
        borrower_name = "Larry",
        loan_days = 5,
        purpose = "Need cash",
        status = "Ready",
):
    return{
        "id": id,
        "equipment_id": equipment_id,
        "borrower_name": borrower_name,
        "loan_days": loan_days,
        "purpose": purpose,
        "status": status,
    }


def test_add_user(client):
    response = client.post("/api/equipment", json=loan_payload())
    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_dup_user(client):
    client.post("/api/equipment", json=loan_payload())

    response = client.post("/api/equipment", json=loan_payload())

    assert response.status_code == 409
    assert "exists" in response.json()["detail"].lower()


def test_get_user(client):
    patient = client.post("/api/equipment", json=loan_payload()).json()
    id = patient["id"]
    response = client.get(f"/api/equipment/{id}")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_missing_user(client):
    response = client.get("/api/equipment/99")

    assert response.status_code == 404
    assert response.json()["detail"] == "Loan not found"


def test_delete_success(client):
    loan = client.post("/api/equipment", json=loan_payload()).json()
    id = loan["id"]
    response = client.delete(f"/api/equipment/{id}")
    assert response.status_code == 204


def test_delete_fail(client):
    response = client.delete("/api/equipment/98")

    assert response.status_code == 404
    assert response.json()["detail"] == "Loan not found"


def test_all_delete(client):
    loan =client.post("/api/equipment", json=loan_payload())

    assert loan.status_code == 201

    id = loan["id"]
    del_loan = client.post(f"/api/equipment/{id}")

    assert del_loan.status_code == 204 

    no_del = client.get(f"/api/equipment/{id}")

    assert no_del.status_code == 404