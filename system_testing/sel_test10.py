#check blog statistics of other users
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

mycomment = "Wonderful"
comment_box = driver.find_element_by_id("tbox_6")
comment_box.send_keys(mycomment)
driver.find_element_by_id("cmtBtn_6").click()
time.sleep(3)
driver.find_element_by_id("same_news").click()

search = driver.find_element_by_id("searchbar")
search.clear()
search.send_keys("va")
time.sleep(3)
driver.find_element_by_class_name("suggest").click()
driver.find_element_by_id("searchbtn").click()
time.sleep(2)

driver.find_element_by_id("id_blog").click()
time.sleep(20)

ale = driver.switch_to_alert()
ale.accept()
time.sleep(5)
driver.close()
