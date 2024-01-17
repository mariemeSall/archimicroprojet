# archi micro projet

## kafka broker
TODO:

[kafka quickstart guide](https://kafka.apache.org/quickstart)

### Data format sent to topic coordinates

The data is to the broker in the format: lat; long; Date.<br>
Example: "-48.744897; -78.637573; 2023-12-27 16:03:41"<br>
This is a full string, so it needs to parsed and converted.

### some command (go into kafka folder)

    i needed to do this to install kafka i guess after cloning repo 

    ./gradlew jar -PscalaVersion=2.13.11

### launch broker on 2 terminal (go into kafka folder first)
    
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

### list topics

	kafka-topics.sh --bootstrap-server localhost:9092 --list --command-config /path/to/client.properties
	
### kafka server logs:
    
    tail -f logs/server.log

### broker config (in server.properties):

    listeners=PLAINTEXT://localhost:9092
    
## Database POSTGRESQL

Once postgres installed
go into BDD, and type createdb coords
if error : "role 'name' does not exist" then create a superuser
by following instructions below and by replacing cytech by
your name.
(to display users: once you type psql type \du)

### create super user for postgresql

    sudo -i -u postgres
    psql
    CREATE USER cytech WITH SUPERUSER CREATEDB CREATEROLE PASSWORD 'password';
    exit
    exit

### create empty database and restore the database into the empty one

    createdb -U cytech coords
    psql -U cytech -d coords -f db_microarchie.dump