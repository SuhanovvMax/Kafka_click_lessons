#!/bin/bash

# Запуск Docker Compose в фоновом режиме
echo "Запуск Docker Compose..."
docker-compose up -d

# Ожидание ввода от пользователя
echo "Нажмите 'n' для остановки Docker Compose"
read input

# Проверка введенной команды
if [ "$input" == "n" ]; then
    echo "Удаление файла meta.properties..."
    docker exec docker_kafka_clickhouse-kafka-1 rm /var/lib/kafka/data/meta.properties
    # Остановка Docker Compose
    echo "Остановка Docker Compose..."
    docker-compose down

else
    echo "Команда '$input' не распознана. Docker Compose продолжает работать."
fi
