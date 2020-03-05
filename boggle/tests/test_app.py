import pytest


@pytest.mark.asyncio
async def test_app_healthcheck(client):
    response = await client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_unpack_request_body(client):
    # Using key `data`, the client will send the request body
    # in the format of b'key=value'
    # which is not a valid JSON format and the server will return a 400 response.
    response = await client.post("/games", data={"key": "value"})
    assert response.status_code == 400
