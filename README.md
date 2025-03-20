# FastAPI_HW
## Описание API
Базовая ссылка для веб-хостинга `https://fastapi-python-alls.onrender.com`, для локального запуска `http://127.0.0.1:8501`
### GET methods
- `/`
  - проверка сервиса
  - формат ответа `{"status": "OK"}`
- `/{short_code}`
  - переход по ссылке, используя зарегистрированный короткий алиас
  - формат ответа при ошибке `{"status":"ERROR: alias {short_code} not found"}`
- `/links/{short_code}/stats`
  - получение статистики по короткому алиасу
  - формат ответа `{'message': str, 'content': {'url': str, 'alias': str, 'created': datetime, 'last_accessed': datetime, 'times_accessed': int, 'expires_at': datetime}}`
- `/links/search?original_url={url}`
  - поиск информации по полной ссылке
  - формат ответа `{'message': str, 'content': {'url': str, 'alias': str, 'created': datetime, 'last_accessed': datetime, 'times_accessed': int, 'expires_at': datetime}}`
- `/links/register`
  - регистрация пользователя для удаления и изменения существующих ссылок
  - обязательные агрументы `headers={"login": str}`
  - формат ответа `{'message': str, 'content': {'login': str, 'token': str}}`
### POST methods
- `/links/shorten`
  - создает алиас для ссылки
  - обязательные аргументы `json={"url": str}`
  - дополнительно можно указать конкретный алиас, к которому будет привызана ссылка `json={"url": str, "alias": str}`
  - формат ответа `{'message': str, 'content': {'url': str, 'alias': str, 'created': datetime, 'last_accessed': datetime, 'times_accessed': int, 'expires_at': datetime}}`
- `/links/{short_code}`
  - присвоение существующей ссылке нового алиаса
  - обязательные аргументы `headers={'login': str, 'token': str}`
  - формат ответа `{'message': str, 'content': {'url': str, 'alias': str, 'created': datetime, 'last_accessed': datetime, 'times_accessed': int, 'expires_at': datetime}}`
### DELETE methods
- `/links/{short_code}`
  - удаление ссылки
  - обязательные аргументы `headers={'login': str, 'token': str}`
  - формат ответа `{'status': 'SUCCESS'}`
## Примеры запросов
Можно найти в файле [test.ipynb][test.ipynb]
## Инструкция по запуску
Для локального запуска необходимо внутри репозитория прописать `docker compose -f ./docker-compose.yml -p fastapi-hw up -d`
## Описание бд
Две таблицы:
1. credentials — информация о зарегистрировавшихся пользователей
  - id      int
  - login   str    логин пользователя
  - token   str    токен пользователя
2. links — информация о ссылках
  - id                  int
  - url                 str        ссылка
  - alias               str        алиас   
  - created             datetime   дата и время добавления ссылки
  - last_accesed        datetime   дата и время время последнего обращения по алиасу
  - times_accesed       int        количество обращений к ссылке по алиасу
  - expires_at          datetime   дата и время время истечения срока жизни ссылки
