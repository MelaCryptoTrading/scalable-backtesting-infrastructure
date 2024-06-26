from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('scenes',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='backtest-group',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for message in consumer:
    scene = json.loads(message.value.decode('utf-8'))
    # Run backtest with the scene parameters
    results = run_backtest(scene)  # Define run_backtest function as per your backtesting logic
    
    # Produce the results back to Kafka
    produce_results(results)

def produce_results(results):
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send('backtest_results', results)
    producer.flush()