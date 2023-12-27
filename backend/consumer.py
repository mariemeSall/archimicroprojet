from confluent_kafka import Consumer, KafkaError
"""
running this will consume the topic coordinates
by simply running when broker is active it should
do the trick.
"""

def consume_messages(bootstrap_servers, group_id, topic):
    consumer_conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])
    
    max_iterations_without_messages = 10
    iterations_without_messages = 0

    try:
        while True:
            msg = consumer.poll(timeout=1000)

            if msg is None:
                iterations_without_messages += 1
                if iterations_without_messages > max_iterations_without_messages:
                    print("No messages received for {} iterations. Exiting.".format(max_iterations_without_messages))
                    break
                else:
                    print("No messages received. Iteration: {}".format(iterations_without_messages))
                continue

            iterations_without_messages = 0  # Reset the count when a message is received

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print("Reached end of partition. Continuing.")
                    continue
                else:
                    print("Error: {}".format(msg.error()))
                    break

            print('Received message: {} --- from partition [{}]'.format(msg.value().decode('utf-8'), msg.partition()))

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        pass

    finally:
        print("Exiting the consumer.")
        consumer.close()

if __name__ == '__main__':
    bootstrap_servers = 'localhost:9092'  # Replace with your Kafka broker's address
    group_id = 'my-consumer-group'  # Choose a unique group ID for your consumer
    TOPIC = 'coordinates'
    consume_messages(bootstrap_servers, group_id, TOPIC)