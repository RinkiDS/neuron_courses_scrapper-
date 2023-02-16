import logging
import mysql.connector


"""this is a class which helps connecting with the mysql database
   """
class sqldb_connection_util:

    @staticmethod
    def get_connection(host, user, password):
        """
        It tries to connect to the database, and if it fails, it logs the error and returns None

        :param host: The hostname of the database server
        :param user: The username to connect to the database with
        :param password: The password for the user
        :return: The connection object is being returned.
        """
        logger = logging.getLogger('ineuron')
        try:

            db = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )

            #print(mydb)
            return db
        except Exception as e:
            logger.info("Connection with Sql Failed", e)

    @staticmethod
    def create_database(host, user, password, name='test2'):
        """
        It creates a database in SQL if it doesn't already exist

        :param host: The hostname of the database server
        :param user: The username of the database
        :param password: The password for the user you're using to connect to the database
        :param name: The name of the database to create, defaults to test2 (optional)
        :return: The database connection is being returned.
        """
        logger = logging.getLogger('ineuron')
        try:
            db = sqldb_connection_util.get_connection(host, user, password)
            cursor = db.cursor()

            sql = "create database IF NOT EXISTS " + name
            #print(sql)
            cursor.execute(sql)
            logger.info("Database SQL Created")
        except Exception as e:
            logger.info("Create database in SQL Failed", e)
        return db

