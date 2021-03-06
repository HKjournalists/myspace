# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import pika
import sys

#定义连接
credentials = pika.PlainCredentials('gdqWeb', 'BigwinWeb')
parameters = pika.ConnectionParameters('192.168.1.96',5672,'/',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print '[x] Waiting for logs. To exit press CTRL+C'

def callback(ch,method,properties,body):
    print "[x] %r" % (body,)

channel.basic_consume(callback,queue=queue_name,no_ack=True)

channel.start_consuming()

