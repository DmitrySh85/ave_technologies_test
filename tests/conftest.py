import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from services.redis_client import get_redis


class FakeRedis:
    def __init__(self):
        self.storage = {}

    async def get(self, key):
        value = self.storage.get(key)
        if value is not None:
            return value.encode()  # имитируем Redis bytes
        return None

    async def set(self, key, value, nx=False):
        if nx and key in self.storage:
            return False
        self.storage[key] = value  # храним str, get() вернёт bytes
        return True

    async def delete(self, key):
        return self.storage.pop(key, None)


# --------------------------
# Фикстуры
# --------------------------
@pytest.fixture
def fake_redis():
    return FakeRedis()


@pytest.fixture
def override_dependencies(fake_redis):
    # переопределяем get_redis на FakeRedis
    app.dependency_overrides[get_redis] = lambda: fake_redis
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client