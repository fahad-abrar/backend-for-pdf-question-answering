from dotenv import load_dotenv
import pika
import os

import pika.exceptions

load_dotenv()
URL = os.getenv('URL')

def callback(channel, method, properties, body):
    data= body.decode()
    print('message received', data)
    channel.basic_ack(delivery_tag = method.delivery_tag)

def consume_content(msg):
    try:
        url = pika.URLParameters(URL)
        connection = pika.BlockingConnection(url)
        channel = connection.channel()

        exchange='elearning'
        queue='question'
        routing_key = 'route-1'

        channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
        channel.queue_declare(queue=queue, durable= False)
        channel.queue_bind(exchange=exchange, queue= queue, routing_key=routing_key)

        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=False)
        print('wating for message...')
        channel.start_consuming()
    
    except pika.exceptions.AMQPError as err:
        print('error connection to rabitmq', err)