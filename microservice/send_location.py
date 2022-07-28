
#!/usr/bin/env python
import pika
import uuid
import json

class MilkshakeRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='myQueue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        self.connection.process_data_events(time_limit=None)
        return str(self.response)

#Testing request milkshake location service; sends location by city, state
milkshake_rpc = MilkshakeRpcClient()

response = milkshake_rpc.call("Redding, California")
print(response)
#MUST STRIP THE BODY CHARS ADDED BY RABBIT MQ, AND NULL TERMINATOR
response = response[2:-1]
print(" [.] Got %r" % json.loads(response))
