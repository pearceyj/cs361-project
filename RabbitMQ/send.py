#!/usr/bin/env python

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                    routing_key='CS361MESSAGE',
                    body='A message from CS361!')
print(" [x] Sent 'A message from CS361!'")

connection.close()
