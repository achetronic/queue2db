#!/usr/bin/env python
import sys, os
from decouple import config
from termcolor import colored
from classes.AMQPController import AMQPController
from classes.MySQLController import MySQLController



# Callback to be executed when a message arrives
def on_message (headers, properties, body):
    try:
        print(" [*] Message received")

        message = {
            "body" : body,
            "headers" : headers,
            "properties" : properties
        }

        if (mysql.StoreMessage(message) != True ):
            raise
    except Exception as error:
        print(" [E] Message not stored on DB")
        print('Caught this error: ' + repr(error))



# Main process
def main():

    # Init Controllers
    print(" [*] Starting controllers")

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
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)