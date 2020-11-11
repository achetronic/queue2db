import mysql.connector as mysql # pip install mysql-connector-python
from datetime import datetime
import json

#
class MySQLController:



    # PUBLIC: Constructor of the class
    # Set credentials and open a connection against AMQP server
    def __init__(self):
        try:
            print(" [-] Starting MySQLController")

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

            if (self.__OpenConnection() != True ):
                raise
            return None
        except:
            print(" [E] MySQLController: Impossible to init the class")
            exit()
        


    # PRIVATE: Open a AMQP connection and store it into the class
    def __OpenConnection(self):
        try:
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
        except:
            print(" [E] MySQLController: Impossible to connect to the server")
            return False



    # PRIVATE: Store a smessage into database
    # Message must be a python dictionary
    def StoreMessage(self, message):
        try:
            # Get a timestamp for inserted row
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Check input message. It must be a dictionary
            for v in message.values():
                if not isinstance(v, dict):
                    raise Exception("Message parameter is not a dictionary object")

            # Convert message into JSON
            message = json.dumps(message)

            # Craft and execute the query
            query = "INSERT INTO " + self.table + " (data, created_at, updated_at) VALUES (%s, %s, %s)"
            query_values = (message, timestamp, timestamp)
            self.cursor.execute(query, query_values)

            # Store the data into DB
            self.connection.commit()

            if( self.cursor.rowcount == 0 ):
                raise

            # No raises, return true
            return True
        except:
            print(" [E] MySQLController: Message was not stored on database")
            return False


        


        