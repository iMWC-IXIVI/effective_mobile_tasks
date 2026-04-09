# АККУРАТНЕЕ С КОМАНДОЙ python manage.py create_users_and_videos из-за копирования файла req.mp4 может занять до 10 минут (размер файла занимаемого на диске 4КБ)

# Настройка проекта:

* __Клонирование проекта__ - ```git clone https://github.com/iMWC-IXIVI/effective_mobile_tasks/```
* __Необходимо перейти в директорию с проектом__ - ```cd effective_mobile_tasks```
* __Создание необходимых папок__ - ```mkdir media\videos```
* __Копирование .env файла (необходимо настроить)__ - ```copy .env_example .env - НАСТРОИТЬ .env```
* __Создание виртуального окружения__ - ```python -m venv venv```
* __Активация виртуального окружения__ - ```venv\Scripts\activate```
* __Загрузка необходимых зависимостей__ - ```pip install -r req.txt```
* __Запуск docker compose__ - ```docker compose up --build```

### PSS
__Если запускаем не для разработки, можно пропустить от пункта "Создание виртуального окружения" до, включительно "Загрузка необходимых зависимостей"__

# Загрузка фикстур и команда:

* __Загрузка пользователей__ - ```docker exec -it django_backend python manage.py loaddata /video_platform/fixtures/users.json``` PS. Пароль от admin 12345
* __Загрузка пользователей рандомных для тестов__ - ```docker exec -it django_backend python manage.py create_users_and_videos```

# Ответы на вопросы:

```text
all() - получение всех объектов
filter() - фильтрация данных
exclude() - исключение данных
save() - сохранение объекта
defer() - отложенная загрузка полей
only() - загрузка только указанных полей
values() - возврат словарей вместо объектов
values_list() - возврат кортежей
select_related() - JOIN для ForeignKey
prefetch_related() - отдельные запросы для ManyToMany
select_for_update() - блокировка записей
get_or_create() - получение или создание
count() - подсчет количества
exists() - проверка существования
```
