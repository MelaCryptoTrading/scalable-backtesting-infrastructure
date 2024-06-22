from kafka import KafkaProducer
import json

def produce_scene(scene):
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send('scenes', scene)
    producer.flush()

scene = {
    'start_date': '2023-01-01',
    'end_date': '2023-12-31',
    'indicator': 'SMA',
    'params': {'period': 15}
}

produce_scene(scene)