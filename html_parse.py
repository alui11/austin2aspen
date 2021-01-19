""" This file contains the functionality for parsing HTML. """
import bs4
from bs4 import BeautifulSoup

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

def traverse_html_tree(tag, extractions):
  """ Helper for HTML parsing functions:
      Given a list of the form [(el_type1, n1), (el_type2, n2), ...], 
      extracts the n1-th top-level occurence of el_type1 in tag, 
      yielding result tag'. Then it will extract the n2-th occurence of 
      el_type2 in tag', yielding tag'', and so on until the list extractions
      is empty. """
  if type(tag) != bs4.element.Tag:
    return tag
  for el_type, n in extractions:
    els = [x for x in tag.contents 
           if type(x) == bs4.element.Tag and x.name == el_type]
    tag = els[n]
  return tag

def get_all_assignment_rows(class_page_soup):
  """ Given HTML soup for the class page containing tables of assignments, 
      returns a list containing each row of those tables as a Tag. """
  all_assignments_ul = [x for x in 
                        class_page_soup.find(
                          "div", {"id": "elementheaders-div"}) 
                        if type(x) == bs4.element.Tag and x.name == 'ul'
                        ][0]
  lists_of_assignments_by_year = [x for x in all_assignments_ul 
                                  if type(x) == bs4.element.Tag 
                                  and x.name == 'li']
  extractions = [('div', -1), ('div', -1), ('div', 1), ('div', 0), 
                 ('table', 0), ('tbody', 0)]
  lists_of_assignments_by_year = list(map((lambda x: 
                                           traverse_html_tree(x, extractions)), 
                                           lists_of_assignments_by_year))
  lists_of_assignments_by_year = list(map(lambda x: x.contents,
                                          lists_of_assignments_by_year))
  return [row for year_list in lists_of_assignments_by_year 
          for row in year_list 
          if type(row) == bs4.element.Tag and row.name == 'tr']

def extract_assignment_links(html):
  """ Parse html and return dictionary of {assignment_name: link_to_results}, 
      for assignments that have been published. """
  assignment2results = dict()
  class_page_soup = BeautifulSoup(html, 'html.parser')
  all_assignments = get_all_assignment_rows(class_page_soup)
  for row in all_assignments:
    cells = [x for x in row.contents if type(x) == bs4.element.Tag 
             and x.name == 'td']
    if cells[9].text != '\ncheck\n':
      continue
    url = cells[3].contents[1].get('href')
    results_page = "https://quest.cns.utexas.edu/instructor/elements/results/show" + url[url.find('?'):]
    assignment_name = cells[3].contents[1].text
    assignment2results[assignment_name] = results_page
  return assignment2results

def extract_student_links(html):
  """Parse html and return dictionary of {student_name: link}."""
  student2link = dict()
  student_soup = BeautifulSoup(html, 'html.parser')
  table_of_students = student_soup.find("table", {"id" : "manual-table"})
  table_of_students = traverse_html_tree(table_of_students, [('tbody', 0)])
  student_link_elements = list(filter(lambda x: type(x) == bs4.element.Tag, 
                                      map(lambda x: 
                                            traverse_html_tree(x, 
                                            [('td', 0), ('a', 0)]), 
                                          table_of_students)))
  for student_link in student_link_elements:
    url = "https://quest.cns.utexas.edu" + student_link.get('href')
    name = student_link.text
    student2link[name] = url
  return student2link

def compute_student_score(html):
  """Given student results page, return the total number of assignment problems that have a nonzero score."""
  results_soup = BeautifulSoup(html, 'html.parser')
  table_of_results = traverse_html_tree(
                      results_soup.find("div", {"id" : "instance-table-div"}), 
                      [('div', 1), ('div', 1), ('div', 0), ('table', 0), 
                        ('tbody', 0)])
  questions_passed = list(filter(
                            lambda x: len(x.text.strip()) != 0 
                                      and x.text.strip() != "0", 
                          map(
                            lambda x: 
                              traverse_html_tree(x, [('td', 3), ('div', 0)]), 
                          filter(
                            lambda x: type(x) == bs4.element.Tag 
                                      and x.name == 'tr' 
                                      and len(x.contents) == 11
                                      and traverse_html_tree(x, [('td', 1)]).text.strip() != 'Withdrawn', 
                          table_of_results.contents))))
  return len(questions_passed)
