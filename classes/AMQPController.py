import pika # pip install pika
from typing import Callable
from decouple import config # pip install python-decouple
from datetime import datetime



class AMQPController:

    # PUBLIC: Constructor of the class
    # Set credentials and open a connection against AMQP server
    def __init__(self):
        try:
            print(" [-] Starting AMQPController")

            server = {
                "host": config('AMQP_SERVER_HOST', default='localhost'),
                "user": config('AMQP_SERVER_USER', default='guest'),
                "pass": config('AMQP_SERVER_PASS', default='guest'),
                "port": config('AMQP_SERVER_PORT', default=5672, cast=int),
                "vhost": config('AMQP_SERVER_VHOST', default='/')
            }
            self.exchange = config('AMQP_EXCHANGE', default='amq.topic')
            self.routingKey = config('AMQP_ROUTING_KEY', default='#')
            self.queue = config('AMQP_QUEUE', default='hello')
            self.consumerTag = config('AMQP_CONSUMER_TAG', default='queue2db-python')
            self.server = server
            self.connection = None
            self.channel = None

            self.allowedProperties = [
                'content_type', 
                'content_encoding', 
                'priority', 
                'correlation_id',
                'reply_to',
                'expiration',
                'message_id',
                'timestamp',
                'type',
                'user_id',
                'app_id',
                'cluster_id'
            ]

            if (self.__OpenConnection() != True ):
                raise
            return None
        except:
            print(" [E] AMQPController: Impossible to init the class")
            exit()
        


    # PRIVATE: Open a AMQP connection and store it into the class
    def __OpenConnection(self):
        try:
            # Set a connection
            credentials = pika.PlainCredentials(self.server['user'], self.server['pass'])
            parameters  = pika.ConnectionParameters(
                self.server['host'], 
                self.server['port'], 
                self.server['vhost'], 
                credentials, 
                heartbeat=0, 
                socket_timeout=None, 
                blocked_connection_timeout=None
            )
            connection = pika.BlockingConnection(parameters)

            # Store connection on the class
            self.connection = connection
            if ( self.connection == None ):
                raise

            # Create the channel
            self.channel = connection.channel()
            if ( self.channel == None ):
                raise

            # Try to craft the exchange
            self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic', passive=False, durable=True)

            # Try to craft the queue on the channel
            self.channel.queue_declare(queue=self.queue, durable=True, exclusive=False, auto_delete=False)

            # Try to bind the exchange and the queue
            self.channel.queue_bind(self.queue, self.exchange, self.routingKey)

            # No raises, return true
            return True
        except Exception as error:
            print(" [E] AMQPController: Impossible to connect to the server")
            #print('Caught this error: ' + repr(error))
            return False



    # PUBLIC: Start a consumer and execute a callback for each message
    # This method pass three arguments (dict objects) to the callback: headers, properties, body
    def Consume(self, callback: Callable = None):
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

            # User gave us a callback?
            if callback == None:
                raise

            # Define a default callback to pass the message filtered to
            def defaultCallback(channel, method, properties, body):
                headers    = self.__ParseMessageHeaders(properties)
                properties = self.__ParseMessageProperties(properties)
                callback(headers, properties, body.decode())

            # Create a consumer
            self.channel.basic_consume(queue=self.queue, on_message_callback=defaultCallback, auto_ack=True, consumer_tag=self.consumerTag+'_'+timestamp)

            # Start consuming
            print(' [*] Consumer started. Waiting for messages.')
            self.channel.start_consuming()
        except Exception as error:
            print(' [*] Consumer stoped.')
            print('Caught this error: ' + repr(error))
            return None



    # PRIVATE: Return a dict object with real properties found on 'properties'
    # properties: <BasicProperties(['delivery_mode=1', "headers={'otro': 'prueba', 'testing': 'testing'}", 'timestamp=23423423432423'])>
    # Method = <Basic.Deliver(['consumer_tag=ctag1.02c08c2697e54a6e945aabaf8f4ae25a', 'delivery_tag=1', 'exchange=', 'redelivered=False', 'routing_key=hello'])>
    def __ParseMessageProperties (self, properties: pika.spec.BasicProperties):
        found_properties = {}
        for property in self.allowedProperties:
            property_value = getattr(properties,property,None)
            if property_value:
                found_properties[property] = property_value
        return found_properties



    # PRIVATE: Return a dict object with headers found on 'properties'
    def __ParseMessageHeaders (self, properties: pika.spec.BasicProperties):
        return properties.headers



    # PRIVATE: Get the raw Pika connection to AMQP
    def __GetConnection(self):
        try:
            return self.connection
        except:
            return None
    


    # PRIVATE: Get the raw Pika channel to AMQP
    def __GetChannel(self):
        try:
            return self.channel
        except:
            return None

        


        