""" This file contains the functionality for parsing HTML. """
import bs4
from bs4 import BeautifulSoup

# sample_HTML = """
# """

def course_info_from_row(course_info_row):
  """ Given Tag object for a table row detailing information about a course, 
      returns (period_num, link_to_course_page) for that course, where
      period number is returned as a string. """
  link_cell = [x for x in course_info_row.contents 
               if type(x) == bs4.element.Tag and x.name == 'td' 
               and len(x.contents) > 1 and x.contents[1].name == 'a'][0]
  link_element = [x for x in link_cell.contents 
                  if type(x) == bs4.element.Tag][0]
  link_to_course_page = ("https://quest.cns.utexas.edu" 
                        + link_element.get('href'))
  period_num = link_element.text.split(" ")[2]
  return period_num, link_to_course_page

def extract_course_links(html):
  """Parse html and return dictionary of {period_no: course link}."""
  periods2links = dict()
  landing_page_soup = BeautifulSoup(html, 'html.parser')
  course_list_table = landing_page_soup.find("table", 
                                            {"id": "courseIndexTable"})
  course_table_body = [x for x in course_list_table.contents 
                      if type(x) == bs4.element.Tag and x.name == 'tbody'][0]
  for course_info_row in course_table_body.contents:
    if type(course_info_row) != bs4.element.Tag:
      continue
    period_num, course_page_link = course_info_from_row(course_info_row)
    periods2links[period_num] = course_page_link
  return periods2links

def extract_assignmentIDs(html):
  """Parse html and return dictionary of {assignment_name: ID}."""
  pass

def extract_assignment_links(html):
  """Calls extract_assignmentIDs and converts IDs to assignment result links. Returns dict of {assignment_name: link}."""
  pass

def extract_student_links(html):
  """Parse html and return dictionary of {student_name: link}."""
  pass

def compute_student_score(html):
  """Given student restuls page, return the total number of assignment problems that have a nonzero score."""
  pass

# if __name__ == "__main__":
#   extract_course_links(sample_HTML)