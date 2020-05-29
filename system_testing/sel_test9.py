#add without all fields(SHOULD BE ABLE TO ADD A POST WITHOUT ANY TAGS)

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
time.sleep(3)

driver.find_element_by_id("id_newpost").click()

newpost = """ ADD NEW POST WITHOUT ANY TAGS """
title = driver.find_element_by_id("title_text")
title.send_keys("JUST TO CHECK")
post = driver.find_element_by_id("post_text")
post.send_keys(newpost)
driver.find_element_by_id("postBtn").click()
time.sleep(2)
ale = driver.switch_to_alert()
ale.accept()
time.sleep(2)
driver.find_element_by_id("id_news").click()
time.sleep(4)
driver.find_element_by_id("id_profile").click()

time.sleep(5)
driver.close()