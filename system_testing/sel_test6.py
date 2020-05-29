#suggestions and user search
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome('./chromedriver')
driver.get("http://localhost/blogstop/index.html")
driver.implicitly_wait(7)

username = driver.find_element_by_name("user")
password = driver.find_element_by_name("pass")

username.clear()
username.send_keys("sparsha")
password.send_keys("spar")
driver.find_element_by_id("s_login_but").click()
time.sleep(5)

search = driver.find_element_by_id("searchbar")
search.send_keys("v")

time.sleep(5)
search.clear()
search.send_keys("vi")
time.sleep(3)
driver.find_element_by_class_name("suggest").click()
driver.find_element_by_id("searchbtn").click()

time.sleep(5)
driver.close()
