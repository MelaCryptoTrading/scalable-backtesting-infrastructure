import mlflow

def kafka_producer_with_mlflow():
    bootstrap_servers = ["localhost:9092"]
    producer_instance = KProducerClass(bootstrap_servers)
    producer = producer_instance.create_producer()
    
    if producer:
        message = {
            "scene_id": "scene1",
            "description": "Backtest scene with SMA indicator",
            "parameters": {
                "start_date": "2022-06-20",
                "end_date": "2024-06-21",
                "indicator": "SMA",
                "window": 20
            }
        }
        message_bytes = json.dumps(message).encode('utf-8')
        topic_name = "scenes"
        
        # Track with MLflow
        mlflow.start_run(run_name="Kafka Producer Run")
        try:
            metadata = producer_instance.publish_message(topic_name, message_bytes)
            logging.info(f"Message metadata: {metadata}")
            mlflow.log_param("topic", topic_name)
            mlflow.log_param("bootstrap_servers", bootstrap_servers)
            mlflow.log_metric("message_size", len(message_bytes))
            mlflow.log_artifact("producer_metadata", metadata)
        except Exception as e:
            logging.error("Failed to publish message")
            mlflow.log_param("status", "failed")
        finally:
            mlflow.end_run()

def kafka_consumer_with_mlflow(topic_name):
    bootstrap_servers = ["localhost:9092"]
    consumer_instance = KConsumerClass()
    consumer = consumer_instance.create_consumer(topic_name, bootstrap_servers)
    
    mlflow.start_run(run_name="Kafka Consumer Run")
    try:
        for message in consumer_instance.read_from_consumer(consumer):
            logging.info(f"Received message: {message.value}")
            mlflow.log_param("topic", topic_name)
            mlflow.log_param("bootstrap_servers", bootstrap_servers)
            mlflow.log_metric("message_offset", message.offset)
            # Process the message
            # For demonstration, log the message content as an artifact
            with open("consumed_message.json", "w") as f:
                f.write(message.value.decode('utf-8'))
            mlflow.log_artifact("consumed_message.json")
    except Exception as e:
        logging.error("Failed to consume message")
        mlflow.log_param("status", "failed")
    finally:
        mlflow.end_run()

if __name__ == "__main__":
    kafka_producer_with_mlflow()
    kafka_consumer_with_mlflow("scenes")


