# Задаем базовый образ (версия не менее версии Python в проекте)
FROM python:3.13

# Задаем рабочую директорию, в которой будет располагаться код
WORKDIR /app

# Устанавливаем poetry
RUN pip install poetry==2.2.1

# копируем файлы с зависимостями в рабочую директорию
COPY pyproject.toml poetry.lock ./

# Отключаем создание нового виртуального окружения
RUN poetry config virtualenvs.create false

# Устанавливаем только зависимости
RUN poetry install --no-root

# Копируем остальной код проекта
COPY . .

# Команда для запуска Django-сервера
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]