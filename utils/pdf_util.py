# Python program to create
# a pdf file

from fpdf import FPDF
import os
import json
import logging

"""this is a class which helps in creating pdf

  """
class pdf_util:

    @staticmethod
    def create_pdf(course_all_data):
        """
        It takes a dictionary as input and creates a pdf file with the same name as the course name

        :param course_all_data: This is the dictionary that contains all the data of the course
        :return: The pdf file name is being returned.
        """

        logger = logging.getLogger('ineuron')

        course_name=str(course_all_data["Course_name"])

        pdf_file_name=os.getcwd()+os.sep+"pdfs"+os.sep+course_name+".pdf"

        pdf = FPDF()
        # Add a page
        pdf.add_page()
        pdf.set_xy(0, 0)

        for key in course_all_data:
            if(key=="Curriculum_data"):
                pass
            else:
                value=course_all_data[key]
                pdf.set_font('arial', 'B', 13.0)
                pdf.multi_cell(0, 5, key + '\n' )
                pdf.ln(5)
                pdf.set_font('arial', 'I', 8.0)
                if(isinstance(value,list)):
                    for i in value:
                        pdf.multi_cell(0, 5, i + " " )
                        pdf.ln(5)

                else:
                    pdf.multi_cell(0, 5, str(value))
                    pdf.ln(5)
          # save the pdf with name .pdf
        pdf.output(pdf_file_name)
        logger.info("PDF Saved!")
        return pdf_file_name

@staticmethod
def write_to_json_file(dictionary):
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)