# Пример файловой структуры

1. В корневой папке создать файл .env
2. Заполнить .env (пример):
```env
HOST_PORT=7654
```
3. Запустить через ```docker compose up --build```
4. Доступен по адресу http://localhost:${HOST_PORT}
5. Подключение к контейнеру с той же машины с хостом localhost и портом DB_CONTAINER_PORT
