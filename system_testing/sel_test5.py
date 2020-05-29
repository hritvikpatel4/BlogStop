#reccomend tags function
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
post = driver.find_element_by_id("post_text")

newpost = """Football is a game that millions of people around the world play and love. It can be called a universal game because every small and big nation plays it.
 Moreover, it’s a great relaxer, stress reliever, teacher of discipline and teamwork. Apart from that, it keeps the body and mind fit and healthy. 
It’s a team game that makes it a more enjoyable game as it teaches people the importance of sportsmanship,Leadership, and unity."""
post.send_keys(newpost)
driver.find_element_by_id("tagBtn").click()
time.sleep(3)
tags = driver.find_element_by_id("disp").text 
tags = tags.split(":")[1]
print("Expected Tags : Sports and Fitness\n", "Recommended tags : ",tags)

driver.close()
