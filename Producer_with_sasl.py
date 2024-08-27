from confluent_kafka import Producer
from project_without_sasl.Connect_DB import connect_CH
import json

config = {
    'bootstrap.servers': 'localhost:9092',  # адрес Kafka сервера
    'client.id': 'simple-producer',
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.username': 'admin',
    'sasl.password': 'admin-secret'
}

producer = Producer(**config)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def send_message(data):
    try:
        # Асинхронная отправка сообщения
        producer.produce('topic_click', data.encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # Поллинг для обработки обратных вызовов
    except BufferError:
        print(f"Local producer queue is full ({len(producer)} messages awaiting delivery): try again")

def receive_data_ch():
    
    client = connect_CH()
    
    data = client.execute('select wh_id, qty_shk from report.safepack_repack_agg limit 100')
    
    for i in data:
        data_json = json.dumps(
            {
                'wh_id' : i[0],
                'qty_shk': i[1]
            }
        )

    send_message(data_json)
    producer.flush()

if __name__ == '__main__':
    receive_data_ch()
