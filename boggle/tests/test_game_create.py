import pytest
from boggle.defaults import DEFAULT_BOARD


@pytest.mark.asyncio
async def test_create_game_random_without_custom_board(client):
    duration = 1800
    random = True
    response = await client.post(
        "/games", json={"duration": duration, "random": random}
    )

    body = response.json()
    assert response.status_code == 201
    assert body["duration"] == duration
    assert body["board"] == DEFAULT_BOARD


@pytest.mark.asyncio
async def test_create_game_random_with_custom_board_random_true(client):
    duration = 1800
    random = True
    board = "A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K"
    response = await client.post(
        "/games", json={"duration": duration, "random": random, "board": board}
    )

    body = response.json()
    assert response.status_code == 201
    assert body["duration"] == duration
    assert body["board"] == DEFAULT_BOARD


@pytest.mark.asyncio
async def test_create_game_with_custom_board(client):
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


@pytest.mark.asyncio
async def test_create_game_no_duration_params(client):
    random = True
    response = await client.post("/games", json={"random": random})

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_fail_create_game_no_random_params(client):
    duration = 1800
    response = await client.post("/games", json={"duration": duration})

    assert response.status_code == 400
