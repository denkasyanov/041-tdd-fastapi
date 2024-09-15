# Create summary


import pytest


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

    response = test_app_with_db.delete("/summaries/0/")
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


@pytest.mark.parametrize(
    "summary_id, payload, status_code, detail",
    [
        [9999999, {"url": "https://foo.bar", "summary": "updated!"}, 404, {"detail": "Summary not found"}],
        [
            0,
            {"url": "https://foo.bar", "summary": "updated!"},
            422,
            {
                "detail": [
                    {
                        "ctx": {"gt": 0},
                        "input": "0",
                        "loc": ["path", "id"],
                        "msg": "Input should be greater than 0",
                        "type": "greater_than",
                    }
                ]
            },
        ],
        [
            1,
            {},
            422,
            {
                "detail": [
                    {"input": {}, "loc": ["body", "url"], "msg": "Field required", "type": "missing"},
                    {"input": {}, "loc": ["body", "summary"], "msg": "Field required", "type": "missing"},
                ]
            },
        ],
        [
            1,
            {"url": "https://foo.bar"},
            422,
            {
                "detail": [
                    {
                        "input": {"url": "https://foo.bar"},
                        "loc": ["body", "summary"],
                        "msg": "Field required",
                        "type": "missing",
                    }
                ]
            },
        ],
        [
            1,
            {"url": "invalid://url", "summary": "updated!"},
            422,
            {
                "detail": [
                    {
                        "ctx": {
                            "expected_schemes": "'http' or 'https'",
                        },
                        "input": "invalid://url",
                        "loc": ["body", "url"],
                        "msg": "URL scheme should be 'http' or 'https'",
                        "type": "url_scheme",
                    }
                ]
            },
        ],
    ],
    ids=["non_existent_summary_id", "invalid_summary_id", "empty_payload", "imcomplete_payload", "invalid_url"],
)
def test_update_summary_invalid(test_app_with_db, summary_id, payload, status_code, detail):
    response = test_app_with_db.put(f"/summaries/{summary_id}/", json=payload)
    assert response.status_code == status_code
    assert response.json() == detail
