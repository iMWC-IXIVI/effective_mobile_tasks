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
all() - получение всех объектов - SELECT * FROM <table>;
filter() - фильтрация данных - SELECT * FROM <table> WHERE <condition>;
exclude() - исключение данных - SELECT * FROM <table> WHERE NOT <condition>;
save() - сохранение нового объекта - INSERT INTO <table> (field1, field2) VALUES (value1, value2);
save() - сохранение существующего объекта - UPDATE <table> SET <field1>=<value1> WHERE <condition>;
defer() - отложенная загрузка полей - defer(<field2>) SELECT <field> FROM <table>; поле field 2 загружается отдельным запросом - SELECT <field2> FROM <table> WHERE <condition>;
only() - загрузка только указанных полей - SELECT <field1>, <field2> FROM <table>;
values() - возврат словарей вместо объектов - SELECT <field 1>, <field 2> FROM <table>; (возвращение списка словарей с данными [{<field>: <value>}, {<field>: <value>}])
values_list() - возврат кортежей - SELECT <field 1>, <field 2> FROM <table>; (возвращение кортежей с данными 
select_related() - JOIN для ForeignKey - SELECT <table1.fields>, <table2.fields> FROM <table> LEFT JOIN <table2> ON <table1.field> = <table2.field>;
prefetch_related() - отдельные запросы для ManyToMany. 3 запроса ниже.
SELECT * FROM <table>;
SELECT * FROM <table1> WHERE <field> IN (<ids>);
SELECT * FROM <table2> WHERE <field> IN (<ids>);
select_for_update() - блокировка записей, создаётся транзакция.
BEGIN;
SELECT * FROM <table> WHERE <condition> FOR UPDATE;
UPDATE <table> SET <field>=<value> WHERE <condition>;
COMMIT;
get_or_create() - получение или создание. Либо получаем, если нет, создаём, 2 запроса
SELECT * FROM <table> WHERE <condition>
INSERT INTO <table> (<field1>, <field2>) VALUES (<value1>, <value2>) 
count() - подсчет количества - SELECT COUNT(*) FROM <table> WHERE <condition>;
exists() - проверка существования - SELECT 1 FROM <table> WHERE <condition> LIMIT 1;
```
