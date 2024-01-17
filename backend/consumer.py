from confluent_kafka import Consumer, KafkaError
"""
message received are like this (str_message in the code):
17.744944; 129.53277; 2024-01-17 11:06:18

"""


def push_msg_to_db(message:str, partition:str):
    splitted_msg = message.split(';')
    lat = splitted_msg[0]
    long = splitted_msg[1]
    date = splitted_msg[2]
    ip = splitted_msg[3]

    return 0

def consume_messages(bootstrap_servers, group_id, topic):
    consumer_conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])
    
    max_iterations_without_messages = 5
    iterations_without_messages = 0

    print('bootstrapped the consumer; waiting for messages')
    try:
        while True:
            msg = consumer.poll(timeout=10)

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
            
            str_message = msg.value().decode('utf-8')
            partition = msg.partition()
            print('Received message: {} --- from partition [{}]'.format(str_message, msg.partition()))
            push_msg_to_db(str_message, partition)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        pass

    finally:
        print("Exiting the consumer.")
        consumer.close()

if __name__ == '__main__':
    bootstrap_servers = 'localhost:9092'  # Replace with your Kafka broker's address
    group_id = 'my-consumer-group'  # Choose a unique group ID for your consumer
    topic = 'coordinates'
    consume_messages(bootstrap_servers, group_id, topic)