import pika
from time import sleep

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
channel = connection.channel()

queue = channel.queue_declare(queue='', exclusive=True)

queue_name = queue.method.queue
exchange_name = 'logs'
channel.queue_bind(exchange='logs', queue=queue_name, routing_key='info')

channel.basic_qos(prefetch_count=1)


def process_message(channel, method, properties, body):
    print(f'RECEIVED: {body.decode()}')
    sleep(body.count(b'*'))
    print('INFO: Done')
    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue=queue_name,
    on_message_callback=process_message
)

print('Waiting for messages...')
channel.start_consuming()
