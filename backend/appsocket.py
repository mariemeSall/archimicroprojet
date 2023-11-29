from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from confluent_kafka import Producer, Consumer, KafkaError
import json 

app = FastAPI()
"""
uvicorn appsocket:app --reload
and do python3 producerws.py to test
TODO: consumer.py qui consume dans topic coordinates
and balance dans bdd PostGRE
Check comment clear un topic
TO MAKE IT ACCESSIBLE FROM OTHER COMPUTERS:
uvicorn appsocket:app --host 0.0.0.0 --port 8000 --reload


"""
# Create a Kafka consumer
consumer_conf = {
    'bootstrap.servers': 'localhost:9092',  # Change this to your Kafka broker address
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest',
}
consumer = Consumer(consumer_conf)
messages = []
# Custom producer with name of machine
machine_identifier = "alan_laptop"

# for message delivery to the broker
def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to topic \'{}\', partition [{}]'.format(msg.topic(), msg.partition()))
    
# produce the data on the broker
def produce_data(data):
    # produce request arguments
    topic = data.get('topic')
    message = data.get('message')
    bootstrap_servers = data.get('bootstrap_servers')

    if not topic or not message or not bootstrap_servers:
        raise HTTPException(status_code=400, detail="Invalid payload")

     # Convert the message to a bytes-like object
    message_bytes = json.dumps(message).encode('utf-8')

    # produce to the broker
    producer_conf = {
        'bootstrap.servers': bootstrap_servers,
    }
    producer = Producer(producer_conf)
    producer.produce(topic, key=machine_identifier, value=message_bytes, callback=delivery_report)
    producer.flush()
    return {"message_produced": f"{message}"}

# ================ WEBSOCKET ================ 
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            # produce with broker
            res = produce_data(data)

            # send a response if needed
            await websocket.send_json(res)
            
    except WebSocketDisconnect:
        print("WebSocket connection closed")