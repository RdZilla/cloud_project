## Как развернуть проект:

> [!WARNING]
> В связи с использованием библиотеки **_Django 5.1.2_** `версия Python должна быть 3.10 и выше`

1. Клонировать репозиторий
   ```shell 
   git clone https://github.com/RdZilla/alert_system.git
   ```

2. Создание виртуального окружения
   ```shell
   python -m venv .venv
   ```
3. Активация виртуального окружения
   ```shell
   .\.venv\Scripts\activate
   ```
4. Обновление пакетного менеджера
   ```shell
   python.exe -m pip install --upgrade pip
   ```
5. Установка Django и зависимых пакетов
   ```shell
   pip install -r .\requirements.txt
   ```
6. Применение миграций
   ``` shell
   python .\manage.py migrate
   ```
7. Запуск проекта
    ```shell
    python .\manage.py runserver
    ```
8. Документация API
   * Swagger доступен по адресу http://localhost:8000/swagger
9. Панель администратора сайта
   * Admin панель доступна по адресу http://localhost:8000/admin
10. База данных пустая
11. Учётные данные суперпользователя:
    * Логин: admin
    * Пароль: admin 

