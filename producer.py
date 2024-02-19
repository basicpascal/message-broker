import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
channel = connection.channel()

# channel.queue_declare(queue='ikbo-26-kalugin')
exchange = channel.exchange_declare(exchange='logs', exchange_type='direct')

message_text = ' '.join(sys.argv[1:]) or 'Empty message'
print(message_text)
channel.basic_publish(
    exchange='logs',
    routing_key='info',
    body=message_text
)

connection.close()
