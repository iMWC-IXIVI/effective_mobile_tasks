# Настройка проекта:

* __Клонирование проекта__ - ```git clone https://github.com/iMWC-IXIVI/effective_mobile_tasks/tree/main/async_task```
* __Необходимо перейти в директорию с проектом__ - ```cd async_task```
* __Создание необходимых папок__ - ```mkdir app\src```
* __Копирование .env файла (необходимо настроить)__ - ```copy .env_example .env - НАСТРОИТЬ .env```
* __Создание виртуального окружения__ - ```python -m venv venv```
* __Активация виртуального окружения__ - ```venv\Scripts\activate```
* __Загрузка необходимых зависимостей__ - ```pip install -r req.txt```
* __Запуск docker compose__ - ```docker compose up --build```

### PSS
__Если запускаем не для разработки, можно пропустить от пункта "Создание виртуального окружения" до, включительно "Загрузка необходимых зависимостей"__

### Таблица с замерами
|            Метрика             | Синхронный код | Асинхронный код | Ускорение |
|:------------------------------:|:--------------:|:---------------:|:---------:|
|       Скачивание файлов        |  4777.75 сек   |   1607.5 сек    | 2.97 раз  |
| Парсинг и загрузка данных в бд |   223.12 сек   |   146.78 сек    | 1.52 раз  |
|          Общее время           |  5000.88 сек   |   1754.29 сек   | 2.85 раз  |
|    Количество записей в бд     |     766737     |     766737      |     -     |

### SQL схема:

|    Название поля     |   Тип поля    |             Ограничения              |                   Описание                   |
|:--------------------:|:-------------:|:------------------------------------:|:--------------------------------------------:|
|          id          |     UUID      | primary_key=True, default=uuid.uuid4 |                Идентификатор                 |
|      code_item       |  String(20)   |            nullable=False            |               Код инструмента                |
|      name_item       |  String(255)  |            nullable=False            |           Наименование инструмента           |
|    basis_delivery    |  String(255)  |            nullable=False            |                Базис доставки                |
|        volume        | DECIMAL(18,6) |            nullable=True             |     Объем договоров в единицу измерения      |
|      volume_rub      | DECIMAL(18,6) |            nullable=True             |            Объем договоров, руб.             |
|   price_change_rub   | DECIMAL(18,6) |            nullable=True             | Изменение цены к цене предыдущего дня (руб.) |
| price_change_percent | DECIMAL(18,6) |            nullable=True             |  Изменение цены к цене предыдущего дня (%)   |
|    minimum_price     | DECIMAL(18,6) |            nullable=True             |               Минимальная цена               |
|      avg_price       | DECIMAL(18,6) |            nullable=True             |            Средневзвешенная цена             |
|    maximum_price     | DECIMAL(18,6) |            nullable=True             |              Максимальная цена               |
|     market_price     | DECIMAL(18,6) |            nullable=True             |                Рыночная цена                 |
|      best_price      | DECIMAL(18,6) |            nullable=True             |       Цена заявки (Лучшее предложение)       |
|     best_demand      | DECIMAL(18,6) |            nullable=True             |          Цена заявки (Лучший спрос)          |
|       counter        |    Integer    |            nullable=True             |            Количество сделок шт.             |
