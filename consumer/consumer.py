from confluent_kafka import Consumer, KafkaError

def consume_messages(bootstrap_servers, group_id, topic):
    consumer_conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(timeout=1000)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            print('Received message: {}'.format(msg.value().decode('utf-8')))

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
    bootstrap_servers = 'localhost:9092'  # Replace with your Kafka broker's address
    group_id = 'my-consumer-group'  # Choose a unique group ID for your consumer
    TOPIC = 'coordinates'
    consume_messages(bootstrap_servers, group_id, TOPIC)
