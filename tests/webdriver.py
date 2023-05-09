from selenium import webdriver
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def add_course_test(course):
    try:
        driver = webdriver.Chrome('/path/to/chromedriver')
        driver.get('https://tigerfocus.onrender.com/testlogin/student')

        time.sleep(1)

        view_courses_button = driver.find_element(By.ID,"add_course_button")
        view_courses_button.send_keys(Keys.ENTER)

        time.sleep(1)

        add_course_button = driver.find_element(By.ID,"add_coursenew_button")
        add_course_button.send_keys(Keys.ENTER)

        time.sleep(1)

        course_code_input = driver.find_element(By.NAME,"course_code")
        course_code_input.send_keys(str(course))

        course_name_input = driver.find_element(By.NAME,"course_name")
        course_name_input.send_keys("test course")

        course_color_input = driver.find_element(By.NAME,"color")
        course_color_input.send_keys("B")
        course_color_input.send_keys(Keys.ENTER)

        time.sleep(1)

        driver.find_element(By.ID,"add_course_button").send_keys(Keys.ENTER)
        time.sleep(1)

        check_string = "// div[contains(text(),\'" + course + "')]"
        check_chip = driver.find_element(By.XPATH, check_string)

        time.sleep(1)

        print("Course, " + check_chip.text + " was added successfully!")

    except NoSuchElementException:
        print("Element does not exist")

    driver.close()

def add_assignment_test(course, assignment, due, time):
    try:
        driver = webdriver.Chrome('/path/to/chromedriver')  
        driver.get('https://tigerfocus.onrender.com/testlogin/student')

        time.sleep(1)

        new_task_button = driver.find_element(By.ID,"create_new_button")
        new_task_button.send_keys(Keys.ENTER)

        time.sleep(1)

        driver.find_element(By.NAME,"course_id").send_keys(Keys.ENTER)
        driver.find_element(By.XPATH, "// option[contains(text(),\'" + course + "'").send_keys(Keys.ENTER)

        assignment_title = driver.find_element(By.NAME,"title")
        assignment_title.send_keys(assignment)

        time.sleep(1)

        due_date_input = driver.find_element(By.NAME,"due_date")
        due_date_input.send_keys(due)
        due_date_input.send_keys(Keys.TAB)
        due_date_input.send_keys(time)
        due_date_input.send_keys(Keys.ENTER)

        time.sleep(1)

        check_string = "// div[contains(text(),\'" + assignment + "')]"
        check_assignment = driver.find_element(By.XPATH, check_string)
        
        time.sleep(2)

        print("Course, " + check_assignment.text + " was added successfully!")

    except NoSuchElementException:
        print("Element does not exist")

    driver.close()


#STUDENT TESTS
course = "COS126"
assignment = "assignment"
add_course_test(course)
add_assignment_test(assignment, course, "0401", "1159P")
