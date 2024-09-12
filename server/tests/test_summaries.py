def test_create_summary(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_create_summary_with_invalid_json(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={})

    assert response.status_code == 422

    print(response.json())
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


def test_read_summary(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})

    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}")
    assert response.status_code == 200

    response_dict = response.json()

    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/summaries/123/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"
