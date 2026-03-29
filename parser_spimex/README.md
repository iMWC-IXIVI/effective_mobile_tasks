# Задача №3. Написать парсер, который скачивает бюллетень по итогам торгов с сайта биржи Spimex.

* Что нужно сделать:

> Достать из бюллетени необходимые столбцы (только из таблицы «Единица измерения: Метрическая тонна», где «Количество Договоров, шт.» > 0)
Получаемые данные:

```text
Код Инструмента (exchange_product_id)
Наименование Инструмента (exchange_product_name)
Базис поставки (delivery_basis_name)
Объем Договоров в единицах измерения (volume)
Объем Договоров, руб. (total)
Количество Договоров, шт. (count)
```

* Сохранение в БД:

> Создать таблицу «spimex_trading_results» со структурой:

```text
id, exchange_product_id, exchange_product_name
oil_id — exchange_product_id[:4]
delivery_basis_id — exchange_product_id[4:7]
delivery_basis_name, delivery_type_id — exchange_product_id[-1]
volume, total, count
date, created_on, updated_on
```

* Требования:

> Создать БД для хранения данных начиная с 2023 года

> При сдаче ментору: время выполнения скрипта и количество записей

> Возможные библиотеки: pandas, xlrd, openpyxl, urllib, ssl
