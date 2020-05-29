#user without any comments error

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#a new user has only 1 post with no comments
try:
    driver = webdriver.Chrome('./chromedriver')
    driver.get("http://localhost/blogstop/index.html")
    driver.implicitly_wait(7)

    username = driver.find_element_by_name("user")
    password = driver.find_element_by_name("pass")

    username.clear()
    username.send_keys("abc")
    password.send_keys("abc")
    driver.find_element_by_id("s_login_but").click()
    time.sleep(3)

    driver.find_element_by_id("id_profile").click()
    driver.find_element_by_id("id_blog").click()
    time.sleep(13)
    time.sleep(5)

finally:
    print("ERRORRR")
    driver.close()