from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from logging.config import fileConfig
from flask_paginate import Pagination, get_page_args

from utils.mongodb_connection_util import mongodb_connection_util as mongoc
from utils.mongodb_operations_util import mongodb_opertaions_util as mongoo
from utils.sqldb_connection_util import sqldb_connection_util as sqlc
from utils.sqldb_operations_util import sqldb_operations_util as sqlo
from utils.course_util import course_util
from utils.pdf_util import pdf_util
from utils.s3_bucket_util import s3_bucket_util

application = Flask('ineuron')

application.config.from_pyfile('config/config.cfg')
fileConfig('config/logging.cfg')
#CORS(app)

app=application

"""
It takes the site_url from the config file, calls the get_all_course function from the course_util file, and then
renders the index.html template with the courses variable
:return: The home function is returning the index.html page.
"""


@app.route("/", methods=['GET'])
def home():
    app.logger.info('Processing all courses Request')
    site_url = app.config["INEURON_SITE_URL"]
    courses = course_util.get_all_course(site_url)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(courses)
    pagination_courses = get_pagination_courses(courses,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('index.html',
                           courses=pagination_courses,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

def get_pagination_courses(courses,offset=0, per_page=10):

    return courses[offset: offset + per_page]


"""It takes the course name from the user and passes it to the get_course_details function in the course_util.py 
file. The get_course_details function returns a dictionary with the course details. The course details are then 
passed to the results.html file :return: The course_data is being returned. """


@app.route("/get_course_details", methods=['GET', 'POST'])
@cross_origin()
def get_course_details():
    app.logger.info('Processing get_course_details Request')
    ineuron_course_url = app.config["INEURON_COURSE_URL"]
    course_data = dict()
    course_name = ""
    if request.method == "POST":
        course_name = request.form["options"]
        # print(course_name,flush=True)
        app.logger.info("Getting info for course " + course_name)
        course_data = course_util.get_course_details(ineuron_course_url, course_name)

    return render_template('results.html', course_data=course_data)


"""It takes the course name from the form, gets the course details from the ineuron website, and then creates a pdf 
file with the course details :return: the render_template function. """


@app.route("/save_data_to_pdf", methods=['GET', 'POST'])
@cross_origin()
def save_data_to_pdf():
    course_name = ""
    print(request.method, flush=True)
    if request.method == "POST":
        course_name = request.form["course"]
    app.logger.info('Processing save data to pdf  Request')
    ineuron_course_url = app.config["INEURON_COURSE_URL"]
    course_data = course_util.get_course_details(ineuron_course_url, course_name)
    pdf_util.create_pdf(course_data)

    return render_template('base.html', result_text="Saved Data to PDF")


"""It takes the course name from the user, fetches the course data from the ineuron website, and saves it to the 
mongo db :return: the rendered template base.html with the result_text as "Saved Data To MongoDB" """


@app.route("/save_data_to_mongo_db", methods=['GET', 'POST'])
@cross_origin()
def save_data_to_mongo_db():
    course_name = ""

    if request.method == "POST":
        course_name = request.form["course"]

    app.logger.info('Processing save data to mongo db Request')
    ineuron_course_url = app.config["INEURON_COURSE_URL"]
    database_name = app.config["MONGO_DB_DATABASE_NAME"]
    collection_name = app.config["MONGO_DB_COLLECTION_NAME"]
    mongo_db_url = app.config["MONGO_DB_URL"]

    save_mongodb(course_name, collection_name, database_name, ineuron_course_url, mongo_db_url)

    return render_template('base.html', result_text="Saved Data To MongoDB")


def save_mongodb(course_name, collection_name, database_name, ineuron_course_url, mongo_db_url):
    """
    It takes the course name, collection name, database name, ineuron course url and mongo db url as input and
    returns the course data in the form of a dictionary.

    :param course_name: Name of the course
    :param collection_name: The name of the collection in which the data will be stored
    :param database_name: The name of the database in which you want to store the data
    :param ineuron_course_url: The url of the course on ineuron
    :param mongo_db_url: The url of the mongodb server
    """
    course_data = course_util.get_course_details(ineuron_course_url, course_name)
    database = mongoc.create_database(mongo_db_url, database_name)
    mongoo.insert_data(database, collection_name, course_data)


"""
It takes the course name from the form, and then calls the save_sql function from the sql_functions.py file, passing it
the course name, the ineuron course url, the sql database name, the sql host, the sql password, the sql table name, and
the sql user
:return: the rendered template base.html with the result_text as "Saved Data to SQL"
"""


@app.route("/save_data_to_mysql", methods=['GET', 'POST'])
@cross_origin()
def save_data_to_mysql():
    course_name = ""

    app.logger.info('Processing save data to SQL  Request')
    sql_database_name = app.config["SQL_DATABASE_NAME"]
    sql_table_name = app.config["SQL_TABLE_NAME"]
    ineuron_course_url = app.config["INEURON_COURSE_URL"]
    sql_host = app.config["SQL_HOST"]
    sql_user = app.config["SQL_USER"]
    sql_password = app.config["SQL_PASSWORD"]

    if request.method == "POST":
        course_name = request.form["course"]

    save_sql(course_name, ineuron_course_url, sql_database_name, sql_host, sql_password, sql_table_name, sql_user)

    return render_template('base.html', result_text="Saved Data to SQL")


def save_sql(course_name, ineuron_course_url, sql_database_name, sql_host, sql_password, sql_table_name, sql_user):
    """
    It takes the course name, course url, sql database name, sql host, sql password, sql table name and sql user as
    input and saves the course name and description in the sql database

    param course_name: The name of the course you want to scrape
    :param ineuron_course_url: The URL of the course on ineuron
    :param sql_database_name: The name of the database you want to create
    :param sql_host: The hostname of the database server
    :param sql_password: The password for the SQL database
    :param sql_table_name: The name of the table in which you want to store the data
    :param sql_user: The username of the SQL database
    """
    course_data = course_util.get_course_details(ineuron_course_url, course_name)
    db = sqlc.create_database(sql_host, sql_user, sql_password, sql_database_name)
    sqlo.create_table(db, sql_database_name, sql_table_name)
    sqlo.insert_data(sql_host, sql_user, sql_password, sql_database_name, sql_table_name,
                     course_data["Course_name"],
                     course_data["Description"])


"""
It takes the course name as input, and saves the data to S3 bucket
:return: the base.html template with the result_text as "Saved Data to S3 Bucket"
"""


@app.route("/save_data_to_S3", methods=['GET', 'POST'])
@cross_origin()
def save_data_to_S3():
    course_name = ""

    app.logger.info('Processing saving data to S3 Bucket Request')
    ineuron_course_url = app.config["INEURON_COURSE_URL"]
    S3_bucket_name = app.config["S3_BUCKET_NAME"]
    S3_access_key = app.config["S3_ACCESS_KEY"]
    S3_secret_key = app.config["S3_SECRET_KEY"]

    if request.method == "POST":
        course_name = request.form["course"]

    saveS2bucket(course_name, S3_access_key, S3_bucket_name, S3_secret_key, ineuron_course_url)

    return render_template('base.html', result_text="Saved Data to S3 Bucket")


def saveS2bucket(course_name, S3_access_key, S3_bucket_name, S3_secret_key, ineuron_course_url):
    """
    It takes the course name, S3 access key, S3 bucket name, S3 secret key and the course url as input and returns the
    course name, pdf file name, sws file name and the course data

    param course_name: The name of the course you want to download
    :param S3_access_key: The access key for your S3 bucket
    :param S3_bucket_name: The name of the bucket you created in S3
    :param S3_secret_key: The secret key of the S3 bucket
    :param ineuron_course_url: The URL of the course on ineuron.ai
    """
    course_data = course_util.get_course_details(ineuron_course_url, course_name)
    course_name = str(course_data["Course_name"])
    pdf_file_name = pdf_util.create_pdf(course_data)

    sws_file_name = course_name + "." + "pdf"
    s3_bucket_util.upload_to_aws(S3_access_key, S3_secret_key, pdf_file_name, S3_bucket_name, sws_file_name)


"""
It takes the course name from the user, fetches the course details from the ineuron website, saves the data to pdf,
saves the data to S3 bucket, saves the data to SQL database and saves the data to mongo db
:return: All Operations Done
"""


@app.route("/do_all_operations", methods=['GET', 'POST'])
@cross_origin()
def do_all_operations():
    course_name = ""

    app.logger.info('Processing Request for doing all operations')
    if request.method == "POST":
        course_name = request.form["course"]

    # 1-Saving Course PDF
    app.logger.info('Processing save data to pdf  Request')
    ineuron_course_url = app.config["INEURON_COURSE_URL"]

    course_data = course_util.get_course_details(ineuron_course_url, course_name)
    pdf_util.create_pdf(course_data)

    # 2-Uploading to S3 Bucket
    app.logger.info('Processing saving data to S3 Bucket Request')
    ineuron_course_url = app.config["INEURON_COURSE_URL"]
    S3_bucket_name = app.config["S3_BUCKET_NAME"]
    S3_access_key = app.config["S3_ACCESS_KEY"]
    S3_secret_key = app.config["S3_SECRET_KEY"]

    saveS2bucket(course_name, S3_access_key, S3_bucket_name, S3_secret_key, ineuron_course_url)

    # 3-Saving data to MYSQL
    app.logger.info('Processing save data to SQL  Request')
    sql_database_name = app.config["SQL_DATABASE_NAME"]
    sql_table_name = app.config["SQL_TABLE_NAME"]
    ineuron_course_url = app.config["INEURON_COURSE_URL"]
    sql_host = app.config["SQL_HOST"]
    sql_user = app.config["SQL_USER"]
    sql_password = app.config["SQL_PASSWORD"]

    save_sql(course_name, ineuron_course_url, sql_database_name, sql_host, sql_password, sql_table_name, sql_user)

    # 4-Saving data to mongoDB
    app.logger.info('Processing save data to mongo db Request')
    ineuron_course_url = app.config["INEURON_COURSE_URL"]
    database_name = app.config["MONGO_DB_DATABASE_NAME"]
    collection_name = app.config["MONGO_DB_COLLECTION_NAME"]
    mongo_db_url = app.config["MONGO_DB_URL"]

    save_mongodb(course_name, collection_name, database_name, ineuron_course_url, mongo_db_url)

    return render_template('base.html', result_text="All Operations Done")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)