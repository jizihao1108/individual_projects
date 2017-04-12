import urllib.request as urllib2
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Open Chrome and go to the pixiv home page
chrome_path = "D:\web developer\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.get('http://www.pixiv.net')
time.sleep(10)

# click on the sign in button
driver.find_element_by_xpath('''//*[@id="wrapper"]/div[2]/div[2]/a[2]''').click()
time.sleep(1)

# Fill in the account information 
username = driver.find_element_by_xpath('''//*[@id="LoginComponent"]/span/form/div[1]/div[1]/input''')
password = driver.find_element_by_xpath('''//*[@id="LoginComponent"]/span/form/div[1]/div[2]/input''')

un = 'xxxxxxxxxxxx' # Your username here
pw = 'xxxxxxxxx' # Your password here

username.send_keys(un) 
password.send_keys(pw)
time.sleep(2)

# click log in button
login_attempt = driver.find_element_by_xpath('''//*[@id="LoginComponent"]/span/form/button''')
login_attempt.submit()
time.sleep(1)

# navigate to daily ranking page
daily_ranking = driver.find_element_by_xpath('''//*[@id="column-misc"]/section[3]/h1/a''')
daily_ranking.click()
time.sleep(5)

# Scroll the daily ranking page twice
for i in range(2):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

# Scrap the source code and use bs4 for further analysis
source = driver.page_source
bstree = bs4.BeautifulSoup(source, 'lxml')

# Add prefix of the main site
main_url = 'http://www.pixiv.net/'

# Initialize 3 lists to store links, author, title
pic_daily_links = []
author_name = []
title_name = []

# Get the required information from html code
list_of_daily_links = bstree.find_all('a', class_='title')
list_of_author_name = bstree.find_all('span', class_='icon-text')
list_of_title_name = bstree.find_all('a', class_='title')

# Loop through each instance and store information in the list
for i in range(len(list_of_daily_links)):
    daily_link = main_url + list_of_daily_links[i].get('href')
    daily_name = list_of_author_name[i].text
    daily_title = list_of_title_name[i].text
    pic_daily_links.append(daily_link)
    author_name.append(daily_name)
    title_name.append(daily_title)

# Further testing code
test_url = pic_daily_links[0]
source_pic = urllib2.urlopen(test_url).read()
bstree_pic = bs4.BeautifulSoup(source_pic, 'lxml')

at_comb = title_name[0] + '/' + author_name[0]

bstree_pic.find_all('img', attrs={'alt': '春にして君を離れ/loundraw'})