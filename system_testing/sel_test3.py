#check comment option
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

print(driver.current_url)


mycomment = "So horrible!"
comment_box = driver.find_element_by_id("tbox_1")
comment_box.send_keys(mycomment)
time.sleep(3)
driver.find_element_by_id("cmtBtn_1").click()
time.sleep(4)
comments = driver.find_element_by_id("cmt_1").text
last_comment = comments.split("\n")[-1]

print("Expected comment : ",mycomment,"\nResult of test : ",last_comment)
driver.close()