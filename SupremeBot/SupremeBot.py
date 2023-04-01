from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time
from info import info
from info import secrets
from info import product



#driver
driver = webdriver.Chrome(executable_path="/Users/Bartus/Documents/chromedriver")


#open website ~3,5sekundy na 2,5s przed dropem
driver.get("https://www.supremenewyork.com/shop/all")
driver.implicitly_wait(10)



#autofill
def autofill(id,part):
    driver.find_element_by_id(id).send_keys(info[part])
def payment(id,part):
    driver.find_element_by_id(id).send_keys(secrets[part])


#Choosing a category
category = driver.find_element_by_link_text(product['category'])
category.click()
time.sleep(1)

# This part gets all the sources from product feed page
URL = driver.current_url
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
page = requests.get(URL, headers=headers)

#needed for bs4
soup = BeautifulSoup(page.content, 'html.parser')


#Key word finder
items = soup.find_all(class_='name-link')

r = u"\u00AE".encode('utf-8')

for a in range(0,len(items)):
    if items[a].get_text() == product['key_word'] and items[a+1].get_text()==product['color']:
        break

selected_item = driver.find_element_by_xpath('''//*[@id="container"]/article[{}]'''.format((a+2)/2))
selected_item.click()


#Getting access to page with the product
URL = driver.current_url
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

sizes = soup.find_all(id='size')

for b in range(0,len(sizes)):
    if items[b].get_text()==product['size']: #elif np Medium albo XLarge
        break


size = driver.find_element_by_xpath('''//*[@id="size"]/option[{}]'''.format(b+1))
size.click()
time.sleep(0.5)

add_to_cart = driver.find_element_by_name('commit')
add_to_cart.click()


try:
    checkout = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'checkout now'))
    )
    checkout.click()
except:
    driver.refresh()




autofill('order_billing_name','name')
autofill('order_email','email')
autofill('order_tel','phone')
autofill('bo','address')
autofill('order_billing_city','city')
autofill('order_billing_zip','postalcode')
payment('cnb','card_number')
payment('vval','cvv')

country = driver.find_element_by_xpath('''//*[@id="order_billing_country"]/option[26]''')
country.click()

card_type = driver.find_element_by_xpath('''//*[@id="credit_card_type"]/option[1]''')
card_type.click()

month = driver.find_element_by_xpath('''//*[@id="credit_card_month"]/option[5]''')
month.click()

year = driver.find_element_by_xpath('''//*[@id="credit_card_year"]/option[2]''')
year.click()

box = driver.find_element_by_xpath('''//*[@id="cart-cc"]/fieldset/p/label/div/ins''')
box.click()











driver.quit()
