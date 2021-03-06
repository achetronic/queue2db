import json
import logging
import mysql.connector as mysql
from decouple import config
from datetime import datetime



class MySQLController:

    # PUBLIC: Constructor of the class
    # Set credentials and open a connection against AMQP server
    def __init__(self):
        try:
            logging.info("[-] MySQLController: Starting controller")

            # Access this with server["port"]
            server = {
                "host": config('MYSQL_SERVER_HOST', default='localhost'),
                "user": config('MYSQL_SERVER_USER', default='root'),
                "pass": config('MYSQL_SERVER_PASS', default='guest'),
                "port": config('MYSQL_SERVER_PORT', default=3306, cast=int),
                "database": config('MYSQL_SERVER_DB', default='queue2db')
            }
            self.table  =  config('MYSQL_TABLE', default='messages')
            self.server = server
            self.connection = None
            self.cursor = None

            # Try to open a connection
            if (self.__OpenConnection() != True ):
                raise

            # Check tables (and create if needed)
            if (self.__CheckTable() == False ):
                if (self.__CreateTable() == False ):
                    raise

            return None
        except Exception as error:
            logging.info("[E] MySQLController: Impossible to init the class")
            logging.debug('[I] MySQLController: ' + repr(error))
            exit()
        


    # PRIVATE: Open a AMQP connection and store it into the class
    def __OpenConnection(self):
        try:
            logging.info("[-] MySQLController: Opening a connection")

            db = mysql.connect(
                host    = self.server['host'],
                user    = self.server['user'],
                passwd  = self.server['pass'],
                db      = self.server['database'],
                port    = self.server['port']
            )

            # Store that connection
            self.connection = db
            if ( self.connection == None ):
                raise

            # Set a cursor on that connection
            self.cursor = db.cursor()
            if ( self.cursor == None ):
                raise

            # No raises, return true
            return True
        except Exception as error:
            logging.info("[E] MySQLController: Impossible to connect to the server")
            logging.debug('[I] MySQLController: ' + repr(error))
            return False



    # PRIVATE: Create a table for messages into database
    def __CheckTable(self):
        try:
            logging.info("[-] MySQLController: Checking table existance")

            query = ("SHOW TABLES LIKE '" + self.table + "'")
            self.cursor.execute(query)

            result = self.cursor.fetchone()
            if not result:
                return False

            return True
        except Exception as error:
            logging.info("[E] MySQLController: Table existance can not be checked")
            logging.debug('[I] MySQLController: ' + repr(error))
            return False



    # PRIVATE: Create a table for messages into database
    def __CreateTable(self):
        try:
            logging.info("[-] MySQLController: Creating the table")

            # Dropping the table if already exists.
            self.cursor.execute('DROP TABLE IF EXISTS ' + self.table)

            # Craft and execute the query
            query = (
                'CREATE TABLE ' + self.table + ' ('
                'id bigint unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY, '
                'data json NOT NULL, '
                'created_at timestamp NULL DEFAULT NULL, '
                'updated_at timestamp NULL DEFAULT NULL)'
            )
            self.cursor.execute(query)

            # Store the changes into DB
            self.connection.commit()

            # No raises, return true
            return True
        except Exception as error:
            logging.info("[E] MySQLController: table for messages was not created")
            logging.debug('[I] MySQLController: ' + repr(error))
            return False



    # PRIVATE: Store a smessage into database
    # Message must be a python dictionary
    def StoreMessage(self, message):
        try:
            logging.info("[-] MySQLController: Storing a message")
            
            # Get a timestamp for inserted row
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Check input message. It must be a dictionary
            # for v in message.values():
            #     if not isinstance(v, dict):
            #         raise Exception("Message parameter is not a dictionary object")

            # Convert message into JSON string
            message = str(json.dumps(message))

            # Craft and execute the query
            query = 'INSERT INTO `'+ self.table +'` (`data`, `created_at`, `updated_at`) VALUES (%s, %s, %s)'
            query_values = (message, timestamp, timestamp)

            self.cursor.execute(query, query_values)

            # Store the data into DB
            self.connection.commit()

            if( self.cursor.rowcount == 0 ):
                raise

            # No raises, return true
            return True
        except Exception as error:
            logging.info("[E] MySQLController: Message was not stored on database")
            logging.debug('[I] MySQLController: ' + repr(error))
            return False


        


        