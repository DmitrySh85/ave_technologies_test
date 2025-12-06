import pytest


@pytest.mark.anyio
async def test_create_phone_success(override_dependencies, async_client):
    payload = {"phone": "+79991112233", "address": "Moscow"}
    response = await async_client.post("/api/v1/phones/", json=payload)

    assert response.status_code == 201
    assert response.json() == payload


@pytest.mark.anyio
async def test_create_phone_conflict(override_dependencies, fake_redis, async_client):
    fake_redis.storage["+79991112233"] = "Old address"
    payload = {"phone": "+79991112233", "address": "New address"}
    response = await async_client.post("/api/v1/phones/", json=payload)

    assert response.status_code == 409


@pytest.mark.anyio
async def test_get_phone_success(override_dependencies, fake_redis, async_client):
    fake_redis.storage["+79991112233"] = "Moscow"
    response = await async_client.get("/api/v1/phones/+79991112233")

    assert response.status_code == 200
    assert response.json() == {"phone": "+79991112233", "address": "Moscow"}


@pytest.mark.anyio
async def test_get_phone_not_found(override_dependencies, async_client):
    response = await async_client.get("/api/v1/phones/+12223334455")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_phone_success(override_dependencies, fake_redis, async_client):
    fake_redis.storage["+79991112233"] = "Old"
    payload = {"address": "New Address"}
    response = await async_client.put("/api/v1/phones/+79991112233", json=payload)

    assert response.status_code == 200
    assert response.json() == {"phone": "+79991112233", "address": "New Address"}


@pytest.mark.anyio
async def test_update_phone_not_found(override_dependencies, async_client):
    payload = {"address": "Whatever"}
    response = await async_client.put("/api/v1/phones/+79991112233", json=payload)
    assert response.status_code == 404


@pytest.mark.anyio
async def test_delete_phone_success(override_dependencies, fake_redis, async_client):
    fake_redis.storage["+79991112233"] = "Value"
    response = await async_client.delete("/api/v1/phones/+79991112233")

    assert response.status_code == 204


@pytest.mark.anyio
async def test_delete_phone_not_found(override_dependencies, async_client):
    response = await async_client.delete("/api/v1/phones/+79991112233")
    assert response.status_code == 404