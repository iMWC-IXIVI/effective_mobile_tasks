## Задание 1. 

### У вас есть таблица users в системе блога.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    country_code CHAR(2),
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE,
    rating INTEGER DEFAULT 0
);
```

* Предположим, в таблице ~1 000 000 записей. Для генерации тестовых данных можно использовать:

```
-- INSERT INTO users (username, email, country_code, registration_date, rating)
-- SELECT ... (генерируемые данные)
```

### Задача:

- Выполните следующий запрос и с помощью EXPLAIN ANALYZE замерьте его время выполнения и стоимость:

> SELECT * FROM users WHERE country_code = 'RU' AND rating > 100;

- Создайте индекс, который, по вашему мнению, максимально ускорит этот запрос. Объясните, почему вы выбрали именно такой тип/комбинацию полей.

- Снова выполните EXPLAIN ANALYZE для того же запроса. Сравните показатели cost, время и использованный план (Seq Scan vs Index Scan).

- Вопрос для размышления: Почему простого индекса на country_code может быть недостаточно? Что происходит с данными после фильтрации по стране?