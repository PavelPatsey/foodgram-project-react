# Проект Foodgram

![Foodgram workflow](https://github.com/PavelPatsey/foodgram-project-react/blob/master/.github/workflows/main.yml/badge.svg)

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
* Скопируйте файл docker-compose.yml и nginx.conf из папки infra на сервер:
```
scp infra/docker-compose.yml <username>@<ip host>:/home/<username>/docker-compose.yml
scp infra/nginx.conf <username>@<ip host>:/home/<username>/nginx.conf
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
    - Заполнить БД начальными данными (необязательно):  
    ```
    sudo docker-compose exec backend python3 manage.py fill_database_with_initial_data
    ```
    - Создать суперпользователя Django:
    ```
    sudo docker-compose exec web python manage.py createsuperuser
    ```
    - Проект будет доступен по IP вашего сервера.
  
## Проект в интернете
Проект запущен и доступен по адресу [http://51.250.109.204/admin/](http://51.250.109.204/admin/)
## Как пользоваться

После запуска проекта, подробную инструкцию можно будет посмотреть по адресу [http://51.250.109.204/redoc/](http://51.250.109.204/redoc/)

В проекте реализована эмуляция почтового сервера, письма сохраняются в папке /sent_emails в головной директории проекта. Для того чтобы посмотреть содержимое писем выполните команду на сервере:
```
sudo docker exec -it <CONTAINER ID контейнера web> bash
```
Перейдите в папку /sent_emails, с помощью команды, прочитайте содержмое лог файла:
```
tail <имя log файла>
```
