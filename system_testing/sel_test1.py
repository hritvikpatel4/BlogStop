#check all links
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
time.sleep(2)
print(driver.current_url)

driver.find_element_by_id("id_newpost").click()
time.sleep(1)
print(driver.current_url)

driver.find_element_by_id("id_news").click()
time.sleep(1)
print(driver.current_url)

driver.find_element_by_id("id_profile").click()
time.sleep(1)
print(driver.current_url)

driver.find_element_by_id("id_logout").click()
time.sleep(2)
print(driver.current_url)
driver.close()

