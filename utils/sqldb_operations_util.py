from  utils.sqldb_connection_util import  sqldb_connection_util as sqlc
import logging


class sqldb_operations_util:

    @staticmethod
    def create_table(db, database_name, table_name):
        """
        It creates a table in the database if it doesn't already exist

        :param db: The database connection object
        :param database_name: The name of the database you want to create
        :param table_name: The name of the table you want to create
        """
        logger = logging.getLogger('ineuron')
        try:
            table_name = database_name + "." + table_name
            sql = "CREATE TABLE IF NOT EXISTS " + table_name + "(name VARCHAR(200), description VARCHAR(3000)) "
            cursor = db.cursor()
            cursor.execute(sql)
        except Exception as e:
            logger.info("Create Table SQl Failed",e)


    @staticmethod
    def insert_data(host,user,password,database_name, table_name, name, description):
        """
        This function takes in the host, user, password, database name, table name, name, and description as parameters and
        inserts the data into the table

        :param host: The hostname of the database server
        :param user: The username of the database
        :param password: The password for the user you're using to connect to the database
        :param database_name: The name of the database you want to connect to
        :param table_name: The name of the table you want to insert data into
        :param name: The name of the database you want to connect to
        :param description: The description of the table
        """
        logger = logging.getLogger('ineuron')
        db = sqlc.get_connection(host,user,password)
        try:
            cursor = db.cursor()
            # logger = logging.getLogger(__name__)
            table_name = database_name + "." + table_name
            sql = "INSERT INTO " + table_name + "(name, description) VALUES (%s, %s)"
            val = (name, description)
            cursor.execute(sql, val)
            db.commit()
            logger.info("SQL Data Inserted")
        except Exception as e:
            print("In Exception", flush=True)
            logger.info("Data Insertion SQL Failed",e)


    @classmethod
    def find_all(cls, dbname, collection_name):
        pass;

    @staticmethod
    def find_by_name(cls, dbname, collection_name, name):
        pass;

    @staticmethod
    def update_name(cls, db, database_name, newname):
        pass;
