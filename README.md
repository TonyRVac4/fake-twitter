<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="">
    <img src="frontend/static/favicon.ico" alt="Logo" width="150" height="150">
  </a>
  <h2 align="center">Fake Twitter</h2>
</div>



## О проекте
Данный проект является очень упрощенным клоном Twitter.

![Product Name Screen Shot][product-screenshot]

### Используемые инструменты
* [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)][docker-url]
* [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)][Python-url]
* [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)][fastapi-url]
* [![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)][pytest-url]
* [![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)][swagger-url]
* [![sqlalchemy](https://www.sqlalchemy.org/img/sqla_logo.png)][sqlalchemy-url]
* [![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)][postgres-url]
* [![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)][redis-url]
* [![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)][nginx-url]


### Особенности работы
Поскольку данная версия прииложения не имеет систему аутентификации используется небольшая фронтенд форма, в которую мы можем подставить api ключ для пользователя на бэкенде.

![Keys][key-form-example-screenshot]

Все endpoint имеют `http-header` с названием `api-key` и frontend автоматически будет подставлять его. 
Ключ вы можете подставить совершенно любой, главное чтобы по нему нашелся пользователь в вашей базе данных. 

Внимание! Изза ошибки в коде фронтенда по умолчанию на бэкэнде обрабатывается пользователь с id 1.

### Возможности приложения
- Пользователь может добавить новый твит.
- Пользователь может удалить свой твит.
- Пользователь может зафоловить другого пользователя.
- Пользователь может отписаться от другого пользователя.
- Пользователь может отмечать твит как понравившийся.
- Пользователь может убрать отметку «Нравится». 
- Пользователь может получить ленту из твитов отсортированных в
порядке убывания по популярности от пользователей, которых он
фоловит.
- Твит может содержать картинку.


## Настройка окружения
1. Для того чтобы запустить это приложение на вашей машине уже должен быть установлен docker.
2. Клонируйте репозиторий на вашу локальную машину:
   ```shell
   git clone https://gitlab.skillbox.ru/alen_koibaev/python_basic_diploma.git
   ```
3. Переименуйте файл `.env.template` на `.env` и установите ваши переменные окружения.
4. В файле `nginx.conf` измените `server_name` параметер на id вашего сервера или `localhost` если запускайте локально.
5. Перейдите в директорию проекта:
   ```shell
   cd python_basic_diploma
   ```
6. Затем соберите образ приложения:
    ```shell
    docker build -t prod-backend-image -f api/Dockerfile-prod api/
    ```

## Запуск
   ```shell
   docker compose up -d
   ```


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[Python-url]: https://www.python.org/
[fastapi-url]: https://fastapi.tiangolo.com/
[postgres-url]: https://www.postgresql.org/
[pytest-url]: https://docs.pytest.org/en/stable/
[swagger-url]: https://fastapi.tiangolo.com/features/
[nginx-url]: https://nginx.org/en/
[sqlalchemy-url]: https://www.sqlalchemy.org/
[redis-url]: https://redis.io/
[docker-url]: https://www.docker.com/
[product-screenshot]: images/demo.png
[key-form-example-screenshot]: images/key-form.png