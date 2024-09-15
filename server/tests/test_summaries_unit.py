from datetime import datetime, timedelta, timezone

from app.api import crud
from tests.conftest import dict_parametrize


some_tz = timezone(timedelta(hours=1))


def test_create_summary(test_app, monkeypatch):
    test_request_payload = {"url": "https://foo.bar"}
    test_response_payload = {"id": 1, "url": "https://foo.bar/"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/summaries/", json=test_request_payload)
    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_summaries_invalid_json(test_app):
    response = test_app.post("/summaries/", json={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "url"],
                "msg": "Field required",
                "input": {},
            }
        ]
    }

    response = test_app.post("/summaries/", json={"url": "invalid://url"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "url_scheme",
                "loc": ["body", "url"],
                "msg": "URL scheme should be 'http' or 'https'",
                "input": "invalid://url",
                "ctx": {"expected_schemes": "'http' or 'https'"},
            }
        ]
    }


def test_read_summary(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "url": "https://foo.bar/",
        "summary": "dummy summary",
        # "created_at": datetime.now(timezone.utc).isoformat(),
        "created_at": datetime.now(some_tz).isoformat(),
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/summaries/9999999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Summary not found"}


def test_read_all_summaries(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "url": "https://foo.bar/",
            "summary": "dummy summary",
            "created_at": datetime.now(some_tz).isoformat(),
        },
        {
            "id": 2,
            "url": "https://bar.foo/",
            "summary": "dummy summary",
            "created_at": datetime.now(some_tz).isoformat(),
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)
    response = test_app.get("/summaries/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_summary(test_app, monkeypatch):
    async def mock_get(id):
        return {
            "id": 1,
            "url": "https://foo.bar/",
            "summary": "dummy summary",
            "created_at": datetime.now(some_tz).isoformat(),
        }

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete(f"/summaries/{1}/")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "url": "https://foo.bar/"}


def test_remove_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/summaries/9999999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Summary not found"}


def test_update_summary(test_app, monkeypatch):
    test_request_payload = {"url": "https://foo.bar", "summary": "updated!"}
    test_response_payload = {
        "id": 1,
        "url": "https://foo.bar/",
        "summary": "updated!",
        "created_at": datetime.now(some_tz).isoformat(),
    }

    async def mock_put(id, payload):
        return test_response_payload

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/summaries/1/", json=test_request_payload)
    assert response.status_code == 200
    assert response.json() == test_response_payload


@dict_parametrize(
    {
        "non_existent_summary_id": {
            "summary_id": 9999999,
            "payload": {"url": "https://foo.bar", "summary": "updated!"},
            "status_code": 404,
            "response_json": {"detail": "Summary not found"},
        },
        "invalid_summary_id": {
            "summary_id": 0,
            "payload": {"url": "https://foo.bar", "summary": "updated!"},
            "status_code": 422,
            "response_json": {
                "detail": [
                    {
                        "type": "greater_than",
                        "loc": ["path", "id"],
                        "msg": "Input should be greater than 0",
                        "input": "0",
                        "ctx": {"gt": 0},
                    }
                ]
            },
        },
        "empty_payload": {
            "summary_id": 1,
            "payload": {},
            "status_code": 422,
            "response_json": {
                "detail": [
                    {"type": "missing", "loc": ["body", "url"], "msg": "Field required", "input": {}},
                    {"type": "missing", "loc": ["body", "summary"], "msg": "Field required", "input": {}},
                ]
            },
        },
        "imcomplete_payload": {
            "summary_id": 1,
            "payload": {"url": "https://foo.bar"},
            "status_code": 422,
            "response_json": {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "summary"],
                        "msg": "Field required",
                        "input": {"url": "https://foo.bar"},
                    }
                ]
            },
        },
        "invalid_url": {
            "summary_id": 1,
            "payload": {"url": "invalid://url", "summary": "updated!"},
            "status_code": 422,
            "response_json": {
                "detail": [
                    {
                        "type": "url_scheme",
                        "loc": ["body", "url"],
                        "msg": "URL scheme should be 'http' or 'https'",
                        "input": "invalid://url",
                        "ctx": {"expected_schemes": "'http' or 'https'"},
                    }
                ]
            },
        },
    }
)
def test_update_summary_invalid(test_app, monkeypatch, summary_id, payload, status_code, response_json):
    async def mock_put(id, payload):
        return None

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(f"/summaries/{summary_id}/", json=payload)
    assert response.status_code == status_code
    assert response.json() == response_json
