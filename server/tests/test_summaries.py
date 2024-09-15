# Create summary


def test_create_summary(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar/"


def test_create_summary_with_invalid_json(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={})

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "url"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }

    response = test_app_with_db.post("/summaries/", json={"url": "invalid://url"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"expected_schemes": "'http' or 'https'"},
                "input": "invalid://url",
                "loc": ["body", "url"],
                "msg": "URL scheme should be 'http' or 'https'",
                "type": "url_scheme",
            }
        ]
    }


# Read summary


def test_read_summary(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})

    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}")
    assert response.status_code == 200

    response_dict = response.json()

    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar/"
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/summaries/9999999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app_with_db.get("/summaries/0/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"gt": 0},
                "input": "0",
                "loc": ["path", "id"],
                "msg": "Input should be greater than 0",
                "type": "greater_than",
            },
        ]
    }


# List summaries


def test_list_summaries(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()

    assert any(summary["id"] == summary_id for summary in response_list)


# Delete summary


def test_delete_summary(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}")
    assert response.status_code == 200

    response = test_app_with_db.delete(f"/summaries/{summary_id}")
    assert response.status_code == 200
    assert response.json()["id"] == summary_id

    response = test_app_with_db.get(f"/summaries/{summary_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_delete_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/summaries/9999999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


# Put summary


def test_update_summary(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = test_app_with_db.put(f"/summaries/{summary_id}/", json={"url": "https://foo.bar", "summary": "updated!"})
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar/"
    assert response_dict["summary"] == "updated!"
    assert response_dict["created_at"]


def test_update_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.put("/summaries/9999999/", json={"url": "https://foo.bar", "summary": "updated!"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary_with_invalid_json(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = test_app_with_db.put(f"/summaries/{summary_id}/", json={})
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "url"],
                "msg": "Field required",
                "type": "missing",
            },
            {
                "input": {},
                "loc": ["body", "summary"],
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }


def test_update_summary_with_incomplete_json(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = test_app_with_db.put(f"/summaries/{summary_id}/", json={"url": "https://foo.bar"})
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "input": {
                    "url": "https://foo.bar",
                },
                "loc": ["body", "summary"],
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }
