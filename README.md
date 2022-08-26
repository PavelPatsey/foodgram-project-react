# Проект Foodgram

![Foodgram workflow](https://github.com/PavelPatsey/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Foodgram реализован для публикации рецептов. Авторизованные пользователи
могут подписываться на понравившихся авторов, добавлять рецепты в избранное,
в покупки, скачать список покупок ингредиентов для добавленных в покупки
рецептов.

## Стек технологий

- проект написан на Python с использованием Django REST Framework;
- библиотека Djoser - аутентификация токенами;
- библиотека django-filter - фильтрация запросов;
- базы данных - PostgreSQL
- система управления версиями - git
- [Docker](https://docs.docker.com/engine/install/ubuntu/), [Dockerfile](https://docs.docker.com/engine/reference/builder/), [Docker Compose](https://docs.docker.com/compose/).

## Проект в интернете
Проект запущен и доступен по адресу [http://130.193.41.48/recipes](http://130.193.41.48/recipes)

Админка доступна по адресу [http://130.193.41.48/admin/](http://130.193.41.48/admin/)

Документация для написания api проекта доступна по адресу [http://130.193.41.48/api/docs/redoc.html](http://130.193.41.48/api/docs/redoc.html)

## Подготовка и запуск проекта
* Склонируйте репозиторий на локальную машину.

### Для работы с удаленным сервером (на ubuntu):
* Выполните вход на свой удаленный сервер.

* Установите docker на сервер:
```
sudo apt install docker.io 
```
* Установите docker-compose на сервер. [Установка и использование Docker Compose в Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-ru)
* Локально отредактируйте файл infra/nginx/default.conf.conf, в строке server_name впишите свой IP
* Скопируйте файлы docker-compose.yml и nginx.conf из папки infra на сервер:
```
scp infra/docker-compose.yml <username>@<ip host>:/home/<username>/docker-compose.yml
scp infra/nginx.conf <username>@<ip host>:/home/<username>/nginx.conf
```
* Скопируйте папку docs на сервер:
```
scp -r docs <username>@<ip host>@130.193.41.48:/home/<username>/
```

* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя на DockerHub>
    
    SECRET_KEY=<секретный ключ проекта django>

    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    SSH_KEY=<ваш SSH ключ (для получения выполните команду: cat ~/.ssh/id_rsa)>
    PASSPHRASE=<если при создании ssh-ключа вы использовали фразу-пароль>

    TELEGRAM_TO=<ID чата, в который придет сообщение, узнать свой ID можно у бота @userinfobot>
    TELEGRAM_TOKEN=<токен вашего бота, получить этот токен можно у бота @BotFather>
    ```
* Workflow состоит из четырех шагов:
     - Проверка кода на соответствие PEP8 и выполнение тестов, реализованных в проекте
     - Сборка и публикация образа приложения на DockerHub.
     - Автоматическое скачивание образа приложения и деплой на удаленном сервере.
     - Отправка уведомления в телеграм-чат.  
  

* После успешного развертывания проекта на удаленном сервере, можно выполнить:
    - Создать суперпользователя Django:
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    ```
    - Импортровать в БД ингредиенты, чтобы пользователи могли ими пользоваться при создании рецептов:  
    ```
    sudo docker-compose exec backend python3 manage.py import_ingredients
    ```
    - Заполнить БД начальными данными (необязательно):  
    ```
    sudo docker-compose exec backend python3 manage.py fill_database_with_initial_data
    ```
    - Проект будет доступен по IP вашего сервера.
