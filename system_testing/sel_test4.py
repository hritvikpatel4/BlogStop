#rendering of plots
import sqlite3
import xml.etree.ElementTree as ET
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

driver.find_element_by_id("id_profile").click()
time.sleep(3)

driver.find_element_by_id("id_blog").click()
time.sleep(20)

ale = driver.switch_to_alert()
ale.accept()


print(driver.current_url)


tree = ET.parse('C:/xampp/htdocs/blogstop/feed.xml')
root = tree.getroot()
print("COMMENTS ON SPARSHA'S POSTS: ")
for p in root.iter('post'):
    if(p.find("user").text=="sparsha"):
        for ele in p.iter('comments'):
            print(ele.text)

print("\n\nPOSTS")
database = r"../pythonsqlite.db"
conn = sqlite3.connect(database)
c = conn.cursor()
c.execute('SELECT * FROM data WHERE username="sparsha"')
all_rows = c.fetchall()
print(all_rows)

time.sleep(20)
driver.close()
