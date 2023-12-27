# archi micro projet

## kafka broker
TODO:

MAKE SURE PRODUCERS CAN PRODUCE IN PARALLEL, NOT THE CASE RIGHT NOW
try asyncio, 2 producer.py files with different keys, try producing
in parallel.

idea: 
producer -> produce request to websocket -> websocket produce on the 'server' machine
the 'server' machine has a consumer which can consume the messages and put them 
in db.

[kafka quickstart guide](https://kafka.apache.org/quickstart)

### Data format sent to topic coordinates

The data is to the broker in the format: lat; long; Date.<br>
Example: "-48.744897; -78.637573; 2023-12-27 16:03:41" <br>
This is a full string, so it needs to parsed and converted.


### launch broker on 2 terminal (go into kafka folder first):
    
    bin/zookeeper-server-start.sh config/zookeeper.properties
    
    bin/kafka-server-start.sh config/server.properties

### test messages on 'test-topic'

write: 

    bin/kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092

read: 

    bin/kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server localhost:9092

### create topic coordinates (one time only):

    bin/kafka-topics.sh --create --topic coordinates --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1

### delete topic

	bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic coordinates

### kafka server logs:
    
    tail -f logs/server.log

### broker config (in server.properties):

    listeners=PLAINTEXT://localhost:9092