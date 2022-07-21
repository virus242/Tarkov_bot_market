import time
from fake_useragent import UserAgent
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={UserAgent().random}")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

def find_p(message):
    url = "https://tarkov-market.com/ru/"
    string = message.text.replace(' ', '_').replace('-', '_').replace(' ', '_')
    try:
        driver.get(url)
        time.sleep(2)

        string_input = driver.find_element_by_xpath('//*[@id="__layout"]/div/div/div/div[2]/div[1]/input')
        time.sleep(5)
        string_input.clear()
        string_input.send_keys('pass')
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        block_things = soup.find(class_="cards-list").find_all("div")[1:]



    except Exception as ex:
        print(ex)

