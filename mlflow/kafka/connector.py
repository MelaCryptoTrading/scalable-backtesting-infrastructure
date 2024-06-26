from kafka.admin.client import KafkaAdminClient


class KafkaConnect():
    def __init__(self):
        pass

    def connect_to_kafka(self):
        """
        Connect to Kafka Cluster on EC2 instance
        """
        client = KafkaAdminClient(bootstrap_servers=["b-2.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092"],
                                  api_version=(0,10,2))
        return client        
        
    def create_topic(self, topic_list, client):
        """
        create topics and add the topics to cluster
        TODO: test this!!!
        """
        client.create_topics(new_topics=topic_list, validate_only=False)

    def fetch_topics_list(self, client):
        """
        return a list of topics from Kafka cluster
        """
        return client.list_topics()
        
    
    def delete_topic(self,client, topic_name):
        """
        delete topic with specific name
        TODO: test this!!!
        """
        client.delete_topics(topic_name)
