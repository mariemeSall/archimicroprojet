from fastapi import FastAPI, HTTPException, BackgroundTasks
from confluent_kafka import Producer, Consumer, KafkaError
import threading
"""
uvicorn app:app --reload
"""
app = FastAPI()

# Create a Kafka consumer
consumer_conf = {
    'bootstrap.servers': 'localhost:9092',  # Change this to your Kafka broker address
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest',
}
consumer = Consumer(consumer_conf)
messages = []

# for message delivery to the broker
def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

@app.post("/produce")
def produce_message(payload: dict):
    # produce request arguments
    topic = payload.get('topic')
    message = payload.get('message')
    bootstrap_servers = payload.get('bootstrap_servers')

    if not topic or not message or not bootstrap_servers:
        raise HTTPException(status_code=400, detail="Invalid payload")

    # produce to the broker
    producer_conf = {
        'bootstrap.servers': bootstrap_servers,
    }
    producer = Producer(producer_conf)
    producer.produce(topic, value=message, callback=delivery_report)
    producer.flush()

    return {"status": "Message received and queued for production"}

@app.get("/consume")
def consume_message(payload: dict):
    # Subscribe to the specified topic
    topic = payload['topic']
    consumer.subscribe([topic])

    # Consume messages
    try:
        while True:
            msg = consumer.poll(1.0)  # 1 second timeout
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            received_message = msg.value().decode('utf-8')
            messages.append(received_message)

            print('Consumed message: {}'.format(received_message))

    except KeyboardInterrupt:
        pass
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

    return {"status": "Messages consumed", "consumed_messages": messages}