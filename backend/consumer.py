from confluent_kafka import Consumer, KafkaError
import psycopg2
from psycopg2 import sql
"""
message received are like this (str_message in the code):
17.744944; 129.53277; 2024-01-17 11:06:18; IP_add

"""

def connect_to_db():
    dbname = "coords"
    user = "cytech"
    password = 'password'
    host = "localhost"
    port = "5432"

    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    return connection

def push_msg_to_db(message: str):
    # Connect to the database
    connection = connect_to_db()

    try:
        # Create a cursor
        with connection.cursor() as cursor:
            # Split the message
            lat, long, date, ip = message.split(';')

            # Insert data into the "coordonnee" table
            insert_query = sql.SQL("""
                INSERT INTO coordonnee (longitude, latitude, date, ip)
                VALUES (%s, %s, %s, %s)
            """)
            cursor.execute(insert_query, (float(long), float(lat), date, ip))

        # Commit the changes
        connection.commit()

    finally:
        # Close the connection
        connection.close()

def retrieve_messages_from_db():
    # Connect to the database
    connection = connect_to_db()

    try:
        # Create a cursor
        with connection.cursor() as cursor:
            # Select all rows from the "coordonnee" table
            select_query = sql.SQL("""
                SELECT * FROM coordonnee
            """)
            cursor.execute(select_query)

            # Fetch all rows
            rows = cursor.fetchall()

            # Return the result
            return rows

    finally:
        # Close the connection
        connection.close()

def clear_all_rows_from_db():
    # Connect to the database
    connection = connect_to_db()

    try:
        # Create a cursor
        with connection.cursor() as cursor:
            # Delete all rows from the "coordonnee" table
            delete_query = sql.SQL("""
                DELETE FROM coordonnee
            """)
            cursor.execute(delete_query)

        # Commit the changes
        connection.commit()

    finally:
        # Close the connection
        connection.close()

# ====================================
# ============ main loop =============
# ====================================
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
            
            # --- message processing ---
            str_message = msg.value().decode('utf-8')
            partition = msg.partition()
            # print('Received message: {} --- from partition [{}]'.format(str_message, msg.partition()))
            push_msg_to_db(str_message)
            print(f'=====\nMESSAGE FROM DB:\n{retrieve_messages_from_db()}')
            # print('clearing...')
            # clear_all_rows_from_db()

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