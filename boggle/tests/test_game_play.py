import pytest


@pytest.mark.asyncio
async def test_game_play_missing_params(client):
    duration = 1800
    random = True
    response = await client.post(
        "/games", json={"duration": duration, "random": random}
    )

    body = response.json()
    assert response.status_code == 201
    assert "board" in body and isinstance(body["board"], str)

    id = body["id"]
    token = body["token"]

    response = await client.put("/games/" + str(id), json={"token": token})

    body = response.json()
    message = "Missing required parameters"

    assert response.status_code == 400
    assert body["message"] == message


@pytest.mark.asyncio
async def test_game_play_word_notfound(client):
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
    search_word = "TEA"

    response = await client.put(
        "/games/" + str(id), json={"token": token, "word": search_word}
    )

    body = response.json()
    message = "The word '{}' is not found in the dictionary".format(search_word)

    assert response.status_code == 400
    assert body["message"] == message


@pytest.mark.asyncio
async def test_game_play_word_found(client):
    duration = 1800
    random = False
    board = "A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K"
    response = await client.post(
        "/games", json={"duration": duration, "random": random, "board": board}
    )

    body = response.json()
    assert response.status_code == 201
    assert body["duration"] == duration
    assert body["board"] == board

    id = body["id"]
    token = body["token"]
    search_word = "eight"
    curr_points = body["points"]

    response = await client.put(
        "/games/" + str(id), json={"token": token, "word": search_word}
    )

    body = response.json()
    assert response.status_code == 200
    assert body["duration"] <= duration
    assert body["points"] == curr_points + len(search_word)
