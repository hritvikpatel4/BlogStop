#likes button
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
like = driver.find_element_by_id("likesBtn_1")
prev = like.text
prev = int(prev.split(":")[1])
expected = prev+1
time.sleep(3)
like.click()
time.sleep(3)
after = like.text
after = int(after.split(":")[1])
print("Expected no of likes : ",expected,"\n Result of test : ",after)
driver.close()