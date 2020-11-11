#!/usr/bin/env python
import sys, os
from classes.AMQPController import AMQPController
from classes.MySQLController import MySQLController

        

# Callback to be executed when a message arrives
def on_message (headers, properties, body):
    # Method = <Basic.Deliver(['consumer_tag=ctag1.02c08c2697e54a6e945aabaf8f4ae25a', 'delivery_tag=1', 'exchange=', 'redelivered=False', 'routing_key=hello'])>
    # Properties = <BasicProperties(['delivery_mode=1', "headers={'otro': 'prueba', 'testing': 'testing'}", 'timestamp=23423423432423'])>
    print(" [x] Message received")

    message = {
        "body" : body,
        "headers" : headers,
        "properties" : properties
    }

    print( message )



    # mysql.StoreMessage({
    #     "h1": "v1",
    #     "h2": "v2"
    # })



# Main process
def main():

    print(" [*] Starting controllers")

    # Init Controllers
    amqp = AMQPController()
    #mysql = MySQLController()
    
    # Process the queue
    amqp.Consume(on_message)
    


# If keys [Ctl] + [C] are pressed. Exit the process
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)