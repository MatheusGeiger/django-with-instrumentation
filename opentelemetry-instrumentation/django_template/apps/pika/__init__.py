import pika

from django_template.settings import STOMP_SERVER_HOST
from django_template.settings import STOMP_SERVER_PASSWORD
from django_template.settings import STOMP_SERVER_PORT_PIKA
from django_template.settings import STOMP_SERVER_USER
from django_template.settings import STOMP_SERVER_VHOST

credentials = pika.PlainCredentials(STOMP_SERVER_USER, STOMP_SERVER_PASSWORD)
parameters = pika.ConnectionParameters(STOMP_SERVER_HOST, STOMP_SERVER_PORT_PIKA, STOMP_SERVER_VHOST, credentials)
connection = pika.BlockingConnection(parameters)
