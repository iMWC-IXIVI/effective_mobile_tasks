# Настройка проекта:

* __Клонирование проекта__ - ```git clone https://github.com/iMWC-IXIVI/effective_mobile_tasks/tree/main/fastapi_task```
* __Необходимо перейти в директорию с проектом__ - ```cd fastapi_task```
* __Копирование .env файла (необходимо настроить)__ - ```copy .env_example .env```
* __Создание виртуального окружения__ - ```python -m venv venv```
* __Активация виртуального окружения__ - ```venv/scripts/activate```
* __Установка зависимостей__ - ```pip install -r req.txt```
* __Перейти в директорию с приложением__ - ```cd app```
* __Запуск сервера__ - ```uvicorn main:app --reload```
