# digitalPlatform
Цифровая академическая платформа для межвузовского обмена: от поиска программы до зачисления

##  Описание

Цифровая платформа для работы с пользователями (студентами) и университетами, с поддержкой иерархии программ, предоставляемых ВУЗами и Swagger-документацией. Система реализована на Flask + SQLAlchemy + PostgreSQL, упакована в Docker-контейнеры.

---

## Функциональность

-  Добавление, удаление и обновление профилей студентов-участников
-  Привязка студентов к программам межвузовского обмена
-  Иерархия программ межвузовского обмена
-  Swagger-документация через Flasgger
-  Docker-окружение для быстрого запуска

---

## Стек технологий

- Python 3.11
- Flask
- SQLAlchemy
- PostgreSQL
- Flasgger (Swagger UI)
- Docker + Docker Compose

---


## Примеры запросов

- Получить всех студентов-участников:
```http
GET /students
```

- Регистрация студента:
```http
POST /students
Content-Type: application/json
{
  "name": "Иван Иванов",
  "email": "ivan@example.com",
  "group_id": 1
}
```

---

##  Быстрый старт (Docker)

1. Клонируй репозиторий:

```bash
git clone https://github.com/your-username/students-api.git
cd students-api
```

2. Запусти:

```bash
docker-compose up --build
```

3. Swagger доступен по адресу:

```
http://localhost:5000/apidocs/
```

---

## Тестирование

```bash
curl -X POST http://localhost:5000/students -H "Content-Type: application/json" \
-d '{"name": "Тестов Тест", "email": "test@example.com", "group_id": 1}'
```

---



---


## Ссылки

- Swagger UI: [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)
