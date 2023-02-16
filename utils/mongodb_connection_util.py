import logging
from pymongo import MongoClient


"""this is a class which helps connecting with the mongodb database

  """
class mongodb_connection_util:
    """
    It takes a connection string as input and returns a MongoDB client object

    :param connection_string: The connection string to the MongoDB server
    :return: The connection object is being returned.
    """
    @staticmethod
    def get_connection(connection_string):
        try:
                logger = logging.getLogger('ineuron')
                mongodb_client= MongoClient(connection_string)
                db = mongodb_client.test
                print(db)
        except Exception as e:
               logger.info("Mongo Db Connection Failed {}".format(e))

        return mongodb_client



        """
        It creates a database in MongoDB
        
        :param connection_string: The connection string to the MongoDB server
        :param name: The name of the database, defaults to test2 (optional)
        :return: The database is being returned.
        """

    @staticmethod
    def create_database(connection_string,name='test2'):
        try:
            logger = logging.getLogger('ineuron')
            mongodb_client=mongodb_connection_util.get_connection(connection_string)
            database = mongodb_client[name]
        except Exception as e:
            logger.info("Database creation in momgodb failed".format(e))

        return database

