from selenium import webdriver
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
driver.get('https://tigerfocus.onrender.com/testlogin/student')

time.sleep(30) # Let the user actually see something!

view_courses_button = driver.find_element(By.ID,"add_course_button")
view_courses_button.click()
time.sleep(5) # Let the user actually see something!
driver.quit()
