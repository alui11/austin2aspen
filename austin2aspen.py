import argparse
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import sys
from time import sleep

import html_parse

parser = argparse.ArgumentParser(description='Flag parser')
parser.add_argument('-p', '--period', type=str, required=True, help='the period number')
parser.add_argument('-a', '--assignment-name', type=str, required=True, help='the name of the assignment')

def sleep_with_progress_bar(sec):
    toolbar_width = sec*10

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    for i in range(toolbar_width):
        sleep(0.1)
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("]\n") # this ends the progress bar

def wait_for_id(driver, element_id, timeout):
    for _ in range(int(timeout/2)):
        try:
            driver.find_element_by_id(element_id)
            return
        except:
            sleep(2)
    print("Error: page failed to render after {} sec. If you have not received the successful login message this may be due to a bad password.".format(timeout))
    sys.exit()

def main():
    args = parser.parse_args()
    uname = input("Enter UTexas username: ")
    pwd = getpass("Enter UTexas password:")

    url = 'https://quest.cns.utexas.edu/instructor/courses'

    # Initialize chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Authenticate
    driver.get(url)
    driver.find_element_by_name("j_username").send_keys(uname)
    driver.find_element_by_name("j_password").send_keys(pwd)
    driver.find_element_by_name("_eventId_proceed").click()
    wait_for_id(driver, "course-table-div", 8)
    print("Successfully logged into UTexas instructor portal.")

    # Get course links
    print("Looking for course periods...")
    for i in range(10):
        try:
            html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            period2courselink = html_parse.extract_course_links(html)
            break
        except:
            if i == 9:
                print("Failed to load page after 10 seconds.")
                sys.exit()
            sleep(1)
    if args.period not in period2courselink:
        print("Error: Period {} not found".format(args.period))
        print("Periods found:")
        for period, _ in sorted(period2courselink.items()):
            print("\t" + period)
        sys.exit()
    print("Found period {}. Looking for assignments...".format(args.period))

    # Get assignment links
    driver.get(period2courselink[args.period])
    for i in range(10):
        try:
            html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            assignment2link = html_parse.extract_assignment_links(html)
            break
        except:
            if i == 9:
                print("Failed to load page after 10 seconds.")
                sys.exit()
            sleep(1)
    if args.assignment_name not in assignment2link:
        print("Error: Assignment {} not found".format(args.assignment_name))
        print("Assignments found:")
        for assignment, _ in sorted(assignment2link.items()):
            print("\t" + assignment)
        sys.exit()
    print("Found assignment {}. Looking for students' results...".format(args.assignment_name))

    # Get student links
    driver.get(assignment2link[args.assignment_name])
    for i in range(10):
        try:
            select = Select(driver.find_element_by_name('manual-table_length'))
            select.select_by_value('100')
            html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            student2link = html_parse.extract_student_links(html)
            break
        except:
            if i == 9:
                print("Failed to load page after 10 seconds.")
                sys.exit()
            sleep(1)
    print("Found students:")
    for student, _ in sorted(student2link.items()):
        if not student.startswith("Lui"):
            print("\t" + student)

    # Get student results
    print()
    print("Printing TSV:")
    print()
    print("StudentName\tScore")
    for student, link in sorted(student2link.items()):
        if not student.startswith("Lui"):
            driver.get(link)
            for i in range(10):
                try:
                    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
                    score = html_parse.compute_student_score(html)
                except:
                    if i == 9:
                        print("Failed to load page after 10 seconds.")
                        sys.exit()
                    sleep(1)
            print("{}\t{}".format(student, score))


if __name__ == "__main__":
    main()
