from confluent_kafka import Consumer, KafkaError
import psycopg2
from psycopg2 import sql
import requests
import httpx
"""
"""

import sys
def pp(*p): # for debug
    for idx, arg_value in enumerate(p): print(f'{idx}:\tval= {arg_value}\ttype= {type(arg_value)}')
    sys.exit()


class Coord:
    def __init__(self, lat, long, ip, date) -> None:
        self.lat: float = lat
        self.long: float = long
        self.ip: str = ip
        self.date: str = date
    

def connect_to_db():
    dbname = "coords"
    user = "root"
    password = "password"
    host = "localhost"
    port = "5432"
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    return connection


def push_to_db(coord: Coord):
    connection = connect_to_db()

    try:
        with connection.cursor() as cursor:
            insert_query = sql.SQL("""
                INSERT INTO coordonnee (longitude, latitude, date, ip)
                VALUES (%s, %s, %s, %s)
            """)
            cursor.execute(insert_query, (coord.long, coord.lat, coord.date, coord.ip))

        connection.commit()

    finally:
        connection.close()
    return {"status": "Message pushed to the database successfully"}


def retrieve_all_rows():
    connection = connect_to_db()

    try:
        with connection.cursor() as cursor:
            select_query = sql.SQL("""
                SELECT * FROM coordonnee
            """)
            cursor.execute(select_query)

            rows = cursor.fetchall()

            return rows

    finally:
        connection.close()


def clear_from_db():
    connection = connect_to_db()

    try:
        with connection.cursor() as cursor:
            delete_query = sql.SQL("""
                DELETE FROM coordonnee
            """)
            cursor.execute(delete_query)

        connection.commit()

    finally:
        connection.close()
    
    return {"status": "All rows cleared from the database"}
    
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

    # start of clean sheets
    clear_from_db()

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
            coord = Coord(lat=lat, long=long, ip=ip, date=date)
            push_to_db(coord)
            all_rows = retrieve_all_rows()

            # convert date in all_rows to string representation
            all_rows_serializable = [
                {"lat": row[1], "long": row[2], "ip": row[3], "date": str(row[4])} for row in all_rows
            ]

            # test api
            response = requests.post("http://127.0.0.1:8000/update_location/", json={"geolocation_data": all_rows_serializable})
            print(f'api response {response.json()}')

            # push the coordinate to the database using FastAPI endpoint
            # response = requests.post("http://127.0.0.1:8000/push_to_db")
            # print(f'POST RESPONSE : {response.json()}')
            # rows = requests.get("http://127.0.0.1:8000/retrieve_all_rows")
            # print(f'---\n{rows}')
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