from kafka import KafkaProducer
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class KProducerClass:
    """
    Create a Kafka producer and send messages to the topic in the cluster.
    """
    
    def __init__(self, bootstrap_servers):
        """
        Initializes the Kafka producer with the provided bootstrap servers.
        
        Args:
            bootstrap_servers (list): List of bootstrap server addresses.
        """
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
    
    def create_producer(self):
        """
        Kafka client that publishes records to the Kafka cluster.
        """
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                retries=5
            )
            logging.info("Kafka producer created successfully.")
        except Exception as ex:
            logging.error("Failed to create Kafka producer.")
            logging.error(str(ex))
        return self.producer
    
    def publish_message(self, topic_name, value_bytes):
        """
        Publishes a message to a Kafka topic.
        
        Args:
            topic_name (str): The name of the topic where the message will be published.
            value_bytes (bytes): The message to be published, in bytes.
        
        Returns:
            RecordMetadata: Metadata of the sent message.
        
        Raises:
            Exception: If there is an error in publishing the message.
        """
        if not self.producer:
            logging.error("Producer not created. Call create_producer() first.")
            return
        
        try:
            # Publish the message to the specified topic
            message = self.producer.send(topic_name, value=value_bytes)
            # Ensure all buffered messages are sent
            self.producer.flush()
            logging.info("Message published successfully.")
            return message.get()
        except Exception as ex:
            logging.error("Exception in publishing message")
            logging.error(str(ex))
            raise

def kafka_producer():
    """
    Function to create a Kafka producer, prepare a message, and send it to a Kafka topic.
    """
    bootstrap_servers = ["localhost:9092"]
    producer_instance = KProducerClass(bootstrap_servers)
    
    # Create the producer
    producer = producer_instance.create_producer()
    
    if producer:
        # Message to send
        message = {
            "scene_id": "scene1",
            "description": "Backtest scene with SMA indicator",
            "parameters": {
                "start_date": "2023-01-01",
                "end_date": "2024-06-21",
                "indicator": "SMA",
                "window": 20
            }
        }
        
        # Prepare message as bytes
        message_bytes = json.dumps(message).encode('utf-8')
        topic_name = "scenes"
        
        # Publish the message
        try:
            metadata = producer_instance.publish_message(topic_name, message_bytes)
            logging.info(f"Message metadata: {metadata}")
        except Exception as e:
            logging.error("Failed to publish message")

if __name__ == "__main__":
    kafka_producer()
