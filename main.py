#!/usr/bin/env python
import sys, os
import logging
from decouple import config
from datetime import datetime
from classes.AMQPController import AMQPController
from classes.MySQLController import MySQLController



# Callback to be executed when a message arrives
def on_message (headers, properties, body):
    try:
        logging.info("[I] Main: Message received")

        message = {
            "body" : body,
            "headers" : headers,
            "properties" : properties
        }

        if (mysql.StoreMessage(message) != True ):
            raise
    except Exception as error:
        logging.error("[E] Message not stored on DB")
        logging.debug('Caught this error: ' + repr(error))
        #print("[E] Message not stored on DB")
        


# Main process
def main():
    #timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    logging.basicConfig(filename='logs/output.log', level=logging.INFO)

    # Init Controllers
    logging.info("[I] Main: Starting controllers")

    global amqp
    global mysql

    amqp = AMQPController()
    mysql = MySQLController()
    
    # Process the queue
    amqp.Consume(on_message)
    


# If keys [Ctl] + [C] are pressed. Exit the process
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("[I] Main: Process interrupted pressing [Ctl] + [C] keys")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)