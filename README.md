# praktikum_new_diplom
yamdb_final
### Описание
Foodgram - сайт для публикации рецептов.
Пользователи могут создавать собственные рецепты, читать рецепты других
пользователей, добавлять рецепты в избранное и список покупок, подписываться
на других пользователей
### Технологии, использованые для реализации бэкенда
- Python 3.10
- Django 3.2
- Django REST Framework
### CD/CI
[Проект можно посмотреть здесь](http://marlo.sytes.net)
[Документация API проекта](http://marlo.sytes.net/api/docs/)
![workflow](https://github.com/vlad-marlo/foodgram-project-react/actions/workflows/main.yml/badge.svg)
### Запуск проекта в dev-режиме
- склонируйте репозиторий и перейдите в него
```
git clone https://github.com/vlad-marlo/foodgram-project-react.git && cd foodgram-project-react
```
- перейти в директорию infra и создать файл .env и оформить по такому образцу
```
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432 
```
- запустить docker-compose ```docker-compose up --build -d```
- выполнить миграции, собрать статику и создать суперпользователя
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py createsuperuser
```
- перезапустить docker-compose
