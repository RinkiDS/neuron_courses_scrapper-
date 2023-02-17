<div id="top"></div>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/RinkiDS">
     
  </a>

<h3 align="center">Ineuron Courses </h3>

  <p align="center">
    Project Files
    <br />
    <a href="https://github.com/RinkiDS/neuron_courses_scrapper-"><strong>Explore the Project »</strong></a>
    <br />
   
  </p>
</div>


<!-- ABOUT THE PROJECT -->
##  About The Project
* Building a Web scraper for iNeuron website to get all courses information.
* Storing the scrapped data to MongoDB.
* Stroing the data in pdf 
* Storing the data in MYSQL
* Building a Flask App to view scrapped data.
* Deploying the app in Azure Elastic bean and AWS.

<!-- USAGE -->
## Usage
*  Web scraping is a term for various methods used to collect data from across the Internet.
*  This web scraper extracts all the data on `iNeuron website's` all course information.
*  The scrapped data is then stored to user specified Mongodb database.

<!-- STEPS -->
## Steps

* Installing Python, PyCharm, Monogodb, Git to Computer.
* Creating Flask app by importing `Flask` module.
* Getting information about iNeuron website.
* Gathering data from most static websites is a relatively straightforward process. However, **dynamic website like iNeuron**, JavaScript is used to load their content. These web pages require a different approach to collecting the desired public data.
* Scraping dynamic website using one of the most popular Python libraries, `BeautifulSoup `which can load the data into Json format by using `"script"` in `soup.find` method.

### Scraping and Inserting to DB
* With the Json data all the required data is stored into Dictionary format.
* Extracted all the course data using loops and stored as list.
* Mongodb Altas is used as DB here, with `pymongo library` mongodb is connected to python.
* Database and collections created via python and the list of dictionaries is uploaded using `collection.insert_many` method.
* Created an `application.py` to initialize

### Flask
* Importing the Flask module and creating a Flask web server from the Flask module.
* Create an object **app** in flask class with `__name__` which represents current app.py file.
* Create `/` route to render all courses with pagination 
* Create a route `/get_course_details to get course data to be is shown in `results.html` page.
* Run the flask app with `app.run()` code.
<p align="right">(<a href="#top">back to top</a>)</p>


### ✨App Screenshot
[![Course List Screen Shot](https://github.com/RinkiDS/neuron_courses_scrapper-/blob/main/static/image/Screenshot%202023-02-17%20115810.png)]<br>
[![Course Details Screen Shot](https://github.com/RinkiDS/neuron_courses_scrapper-/blob/main/static/image/Screenshot%202023-02-17%20120009.png)]
[![Sample PDF File](https://github.com/RinkiDS/neuron_courses_scrapper-/blob/main/pdfs/Face%20Swap%20Application.pdf)]





### Technologies used**
[![Language | Python](https://img.shields.io/badge/Python-eeeeee?style=for-the-badge&logo=python&logoColor=ffffff&labelColor=3776AB)][python]
[![Framework & Library | Flask](https://img.shields.io/badge/Flask-eeeeee?style=for-the-badge&logo=flask&logoColor=000000&labelColor=fefefe)][flask]
[![Language | MongoDB](https://img.shields.io/badge/Mongo_DB-eeeeee?style=for-the-badge&logo=mongodb&logoColor=47A248&labelColor=fefefe)][mongodb]

### 🔧 **Tools used**
[![Tools used | PyCharm](https://img.shields.io/badge/PyCharm-eeeeee?style=for-the-badge&logo=PyCharm&logoColor=008000&labelColor=2C2C32)][PyCharm]
[![Tools used | Git](https://img.shields.io/badge/Git-eeeeee?style=for-the-badge&logo=git&logoColor=F05032&labelColor=f0efe7)][git]

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
Contact

<a href="https://www.linkedin.com/in/rinki-sharma-79102119/?trk=public-profile-join-page"></a>LinkedIN Contact<br>
<a href="mailto:rinki.sharma@gmail.com?subject=Github"/>Gmail Contact


<!-- ACKNOWLEDGMENTS -->
     Acknowledgments





<!-- MARKDOWN LINKS  -->

<!-- Tools Used -->
[PyCharm]: https://code.visualstudio.com/
[git]: https://git-scm.com/
[github]: https://github.com/
[microsoft_azure]: https://azure.microsoft.com/en-in/features/azure-portal/
[python]: https://www.python.org/
[mongodb]: https://www.mongodb.com/
[flask]: https://flask.palletsprojects.com/en/2.1.x/



