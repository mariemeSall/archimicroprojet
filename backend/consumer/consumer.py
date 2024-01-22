from confluent_kafka import Consumer, KafkaError
from pydantic import BaseModel
import requests

class Coord(BaseModel):
    lat: float
    long: float
    ip: str
    date: str

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

    print(f'bootstrapped the consumer to broker and topic [{topic}]; waiting for messages...')
    try:
        while True:
            msg = consumer.poll(timeout=10)
            
            # exit after too much idle time
            if msg is None:
                iterations_without_messages += 1
                if iterations_without_messages > max_iterations_without_messages:
                    print("No messages received for {} iterations. Exiting.".format(max_iterations_without_messages))
                    break
                else:
                    print("No messages received. Iteration: {}".format(iterations_without_messages))
                continue

            iterations_without_messages = 0  # Reset the count when a message is received

            # error handling
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print("Reached end of partition. Continuing.")
                    continue
                else:
                    print("Error: {}".format(msg.error()))
                    break
            
            # parse message
            splitted_message = msg.value().decode('utf-8').split(';')
            lat = float(splitted_message[0])
            long = float(splitted_message[1])
            ip = splitted_message[2]
            date = splitted_message[3]
            # turn it into object
            body = Coord(lat=lat, long=long, ip=ip, date=date)
            print(body)

            # push the coordinate to the database using FastAPI endpoint
            response = requests.post("http://127.0.0.1:8000/push_to_db")
            print(f'POST RESPONSE : {response.json()}')
            rows = requests.get("http://127.0.0.1:8000/retrieve_all_rows")
            print(f'---\n{rows}')
            # TODO: Push to map map in frontend the rows that will autoupdate the map based on the coords
            
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        pass

    finally:
        print("Exiting the consumer.")
        consumer.close()

if __name__ == '__main__':
    bootstrap_servers = 'localhost:9092'  # Kafka broker's address
    group_id = 'my-consumer-group'
    topic = 'coordinates'
    consume_messages(bootstrap_servers, group_id, topic)