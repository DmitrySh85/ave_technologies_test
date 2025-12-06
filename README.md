# Phone-Address Microservice

Микросервис для хранения и управления связками **телефон-адрес**.  
Позволяет быстро сохранять, получать, обновлять и удалять адреса по номеру телефона.

---

## 🛠 Технологии и стек

- **Python 3.13**
- **FastAPI** — REST API
- **Redis** — быстрое хранилище ключ-значение
- **Docker & Docker Compose** — для контейнеризации и быстрого запуска
- **pytest + httpx + anyio** — тестирование асинхронных эндпоинтов
- **Pydantic** — валидация и сериализация данных
- **Logging** — логирование операций (INFO/WARNING)

---

## 🔹 Функциональность

Сервис предоставляет CRUD операции:

| Метод | Эндпоинт | Описание |
|-------|----------|---------|
| GET | `/api/v1/phones/{phone_number}` | Получить адрес по телефону |
| POST | `/api/v1/phones/` | Создать новую связку телефон-адрес |
| PUT | `/api/v1/phones/{phone_number}` | Обновить адрес для существующего номера |
| DELETE | `/api/v1/phones/{phone_number}` | Удалить запись по номеру |

**Валидация номера телефона**:

- Должен начинаться с `+`
- Содержать только цифры
- Длина: 12 символов

**HTTP коды:**

- `200 OK` — успешное получение или обновление
- `201 Created` — успешное создание
- `204 No Content` — успешное удаление
- `404 Not Found` — запись не найдена
- `409 Conflict` — запись уже существует при создании

---

## ⚙️ Установка и запуск

### 1. Клонируем репозиторий

```bash
git clone https://github.com/DmitrySh85/ave_technologies_test.git
cd ave_technologies_test

2. Создаём .env файл
cp .env.example .env
Заполнить по образцу из .env.example

3. Запуск через Docker Compose
docker-compose up --build -d
FastAPI будет доступен на http://localhost:8001

Документация Swagger: http://localhost:8000/docs

🧪 Тестирование

pytest -v
Используется FakeRedis для мокирования Redis в тестах

Все CRUD эндпоинты покрыты тестами

🔹 Примеры запросов
GET
curl http://localhost:8000/api/v1/phones/+79991112233



POST
curl -X POST http://localhost:8000/api/v1/phones/ \
-H "Content-Type: application/json" \
-d '{"phone": "+79991112233", "address": "Moscow"}'


PUT
curl -X PUT http://localhost:8000/api/v1/phones/+79991112233 \
-H "Content-Type: application/json" \
-d '{"address": "Saint Petersburg"}'


DELETE
curl -X DELETE http://localhost:8000/api/v1/phones/+79991112233
📌
 
 Особенности
Асинхронная работа с Redis через redis.asyncio

Логирование всех операций (INFO/WARNING)

Dockerized сервис, готовый к развертыванию

Тесты покрывают все основные сценарии