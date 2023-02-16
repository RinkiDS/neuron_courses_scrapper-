import json
import logging
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs


"""This is a util class which is used to get all course related details"""
class course_util:

    @staticmethod
    def get_all_course(url):
        """
        It scrapes the website and returns a list of all the courses available on the website

        :param url: The url of the page to get all courses
        :return: A list of all the courses available on the website.
        """

        try:
            logger = logging.getLogger('ineuron')
            uClient = uReq(url)
            ineuron_page = uClient.read()
            uClient.close()
            ineuron_html = bs(ineuron_page, 'html.parser')
            course_data = json.loads(ineuron_html.find(
                'script', {"id": "__NEXT_DATA__"}).get_text())
            all_courses = course_data['props']['pageProps']['initialState']['init']['courses']
            course_namelist = list(all_courses.keys())
            logger.info("All Courses Retrieved!")
            return course_namelist
        except Exception as e:
            logger.info("Courses retrieval failed {}".format(e))

    @staticmethod
    def get_course_details(url, course_name):
        """
        It takes the url of the course and the name of the course as input and returns a dictionary containing all the
        details of the course

        :param url: The url of the website from where you want to scrape the data
        :param course_name: The name of the course you want to get details for
        :return: A dictionary with the following keys:
            Course_name
            Description
            Language
            Pricing
            Curriculum_data
            Syllabus
            Requirements
        """

        logger = logging.getLogger('ineuron')
        course_name = str(course_name).replace(" ", "-")
        url = url + "/" + course_name
        uClient = uReq(url)
        course_page = uClient.read()
        uClient.close()
        ineuron_html = bs(course_page, 'html.parser')
        course_all_data = json.loads(ineuron_html.find(
            'script', {"id": "__NEXT_DATA__"}).get_text())
        logger.info('Course Data Retrieved!')
        course_dict = {}
        no_data_present = "No data Available"
        course_description = ""
        try:
            course_all_data = course_all_data["props"]["pageProps"]
            course_data = course_all_data['data']
            course_detail = course_data['details']
            course_meta_data = course_data['meta']
            course_curriculum = checkKey(course_meta_data, "curriculum")
            course_overview = checkKey(course_meta_data, 'overview')
            course_pricing_inr = checkKey(course_detail, 'pricing')
            if (course_pricing_inr["isFree"] != True):
                course_pricing_inr = course_pricing_inr['IN']
            else:
                course_pricing_inr = "FREE COURSE"

            course_name = checkKey(course_data, 'title')
            course_description = checkKey(course_detail, 'description')
            course_language = checkKey(course_overview, 'language')
            course_requirement = checkKey(course_overview, 'requirements')
            course_learning = checkKey(course_overview, 'learn')
        except Exception as e:
            logger.info("Courses data retrieval failed {}".format(e))
            curriculum = []
            try:
                for i in course_curriculum:
                    curriculum.applicationend(course_curriculum[i]["title"])
            except:
                curriculum.applicationend(no_data_present)

        course_dict = {"Course_name": course_name, "Description": course_description,
                       "Language": course_language, "Pricing": course_pricing_inr,
                       "Curriculum_data": course_curriculum, "Syllabus": course_learning,
                       "Requirements": course_requirement}


        return course_dict


def checkKey(dic, key):
    """
    It takes a dic and key as input and returns value from dic if present else blank.
    Args:
    dic : object of dic
    key: key in dic
    Returns:
    value of dic[key]
    """
    value = "No Info"
    if key in dic.keys():
        value = dic[key]
    else:
        value = "No Information"
    return value
