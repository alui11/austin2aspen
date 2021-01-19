import argparse
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
from time import sleep

parser = argparse.ArgumentParser(description='Flag parser')
parser.add_argument('-p', '--period', type=int, required=True, help='the period number')
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

def main():
    args = parser.parse_args()
    uname = input("Enter UTexas username: ")
    pwd = getpass("Enter UTexas password:")

    url = 'https://quest.cns.utexas.edu/instructor/courses'

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    actual_url = driver.current_url
    while actual_url != url:
        driver.find_element_by_name("j_username").send_keys(uname)
        driver.find_element_by_name("j_password").send_keys(pwd)
        driver.find_element_by_name("_eventId_proceed").click()
        sleep_with_progress_bar(5)
        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        actual_url = driver.current_url
        if actual_url != url:
            print("Error: Bad username or password.")
            pwd = getpass("Retry password:")
    print("Success")


if __name__ == "__main__":
    main()
