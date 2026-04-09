# Задание: REST API для видеоплатформы

> Необходимо написать приложение для работы с видео, которое позволит пользователям просматривать видео и ставить лайки. Приложение должно быть реализовано с использованием Django REST Framework и предоставлять REST API.

### Сущности (Models):

1. #### Video:
```text
owner (ForeignKey User, CASCADE)
is_published (BooleanField, default=False)
name (CharField, max_length=100)
total_likes (IntegerField, default=0)
created_at (DateTimeField, auto_now_add=True)
```

2. #### VideoFile:
```text
video (ForeignKey Video, CASCADE, related_name='files')
file (FileField, upload_to='videos/')
quality (CharField, choices=[('HD', 'HD'), ('FHD', 'FHD'), ('UHD', 'UHD')], default='HD')
```

3. #### Like
```text
video (ForeignKey Video, CASCADE)
user (ForeignKey User, CASCADE)
Уникальный ограничитель: (video, user) - unique_together
```

### ViewSet Endpoints (6 штук):

1. #### GET /v1/videos/{video.id}/
```text
Получение конкретного видео по ID
Для is_published=False доступен только owner
При no content возвращать 404
Иметь возможность получать данные пользователя: ?user_expand=true
```

2. #### GET /v1/videos/
```text
Получение списка всех видео
В ответе должны быть: id, name, created_at, owner_id
ВАЖНО: Использовать только select_related/prefetch_related для оптимизации запросов
```

3. #### POST /v1/videos/{video.id}/likes/
```text
Поставить лайк видео
Нельзя ставить лайк самому себе
Повторный лайк должен выдавать 400 Bad Request
При успешном создании лайка увеличивать total_likes у видео на +1
```

4. #### GET /v1/videos/ids/
```text
Получение списка ID всех опубликованных видео
В ответе должен быть список: [1, 2, 3, ...]
```

5. #### GET /v1/videos/statistics-subquery/
```text
Получение статистики с использованием Subquery
В ответе для каждого видео: id, total_likes
Обязательно: Использовать Subquery + OuterRef для подсчета лайков
```

6. #### GET /v1/videos/statistics-group-by/
```text
Получение статистики с использованием GROUP BY
В ответе для каждого видео: id, total_likes
Обязательно: Использовать annotate + values для группировки
```

### Аутентификация и Авторизация
#### Три уровня прав доступа для endpoint /v1/videos/{video.id}/:
```text
is_published=True: доступен всем (даже неавторизованным)
is_published=False + owner=user: доступен владельцу
is_published=False + owner≠user: доступ запрещен (403 Forbidden)
> Использовать Django REST Framework permissions
> Реализовать Custom Permission класс для контроля доступа
```

### Админ панель
```text
Реализовать admin.py для всех трех моделей (Video, VideoFile, Like)
Добавить отображение relevant полей в списке и детальном просмотре
Добавить фильтры и поиск для удобства управления контентом
Оптимизировать запросы в админке (select_related/prefetch_related)
```

### Дополнительные требования

#### Dockerfile:
```text
Создать Dockerfile для приложения
Использовать официальное Python base image
Прописать requirements.txt с зависимостями
Настроить работу с PostgreSQL
Оптимизировать слои (кэширование dependencies)
```

### Структура проекта:
```text
Следовать best practices Django проекта
Разделение settings (dev/prod/test)
Правильная организация apps (configuration в apps.py)
Использование management commands
```

### SQL Query Logging:
```text
Настроить логирование SQL запросов (development mode)
Использовать django-extensions или custom middleware
Проверять количество запросов на каждом endpoint
```

### Тестовые данные:
```text
Создать management command для генерации тестовых данных
Сгенерировать 100k опубликованных видео для 10k пользователей
Создать распределение лайков (random, но реалистичное)
```

### Разбор ORM запросов

#### Для каждого из следующих методов Django ORM объяснить, какие SQL запросы они генерируют и когда:
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

### (Опционально) Тесты
```text
Написать тесты для ключевых endpoints
Использовать pytest + pytest-django или APITestCase
Протестировать permissions и аутентификацию
Проверить оптимизацию запросов (assertNumQueries)
Тесты на создание лайков и защиту от повторных лайков
```

---

# [Настройка проекта](./README_INIT.md)
