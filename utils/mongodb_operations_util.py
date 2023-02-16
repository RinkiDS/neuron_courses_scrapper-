import logging

"""this is a class which helps performing operations with the mongodb database

  """


class mongodb_opertaions_util:
    logger = None

    @staticmethod
    def insert_data(database,collection_name,data):
        """
        It takes a database, a collection name, and a data dictionary as input, and inserts the data into the collection

        :param database: The name of the database you want to connect to
        :param collection_name: The name of the collection in which you want to insert the data
        :param data: The data to be inserted into the database
        """
        logger = logging.getLogger('ineuron')

        try:
            collection=database[collection_name]
            collection.insert_one(data)
            logger.info("MongoDB Data Inserted")
        except Exception as e:
            logger.info("Exception in insert mongodb data",e)
       
    @staticmethod
    def find_all(dbname,collection_name):
        collection=dbname[collection_name]
        x = collection.find_one()
        for i in collection.find():
            print(i)
    
    @staticmethod
    def find_by_name(dbname,collection_name,name):
        pass;
    @staticmethod
    def update_name(database,collection_name,newname):
        pass;