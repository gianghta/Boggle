import pytest

from boggle.defaults import DEFAULT_BOARD


@pytest.mark.asyncio
async def test_game_show(client):
    duration = 1800
    random = True
    response = await client.post(
        "/games", json={"duration": duration, "random": random}
    )

    body = response.json()
    assert response.status_code == 201
    assert body["duration"] == duration
    assert body["board"] is not None

    id = body["id"]
    token = body["token"]

    response = await client.get("/games/" + str(id))

    body = response.json()

    assert response.status_code == 200
    assert body["board"] == DEFAULT_BOARD
    assert body["points"] is not None
    assert body["duration"] <= duration
    assert body["token"] == token
    assert body["id"] == id
    assert body["points"] is not None
