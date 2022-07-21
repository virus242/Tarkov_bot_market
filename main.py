import telebot
import time
from fake_useragent import UserAgent
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

TOKEN = 'TOKEN'     # your token
bot = telebot.TeleBot(TOKEN)    # creating a bot

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={UserAgent().random}")    # random user agent
options.headless = True     # background browser work

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


@bot.message_handler(commands=['start', 'help'])    # response to "/start" and "/help"
def start(message):
    bot.send_message(message.chat.id, 'Hello! To search you need to \n enter the command "/find"')


@bot.message_handler(commands=['find'])
def find(message):
    msg = bot.send_message(message.chat.id, "What item to find?")
    bot.register_next_step_handler(msg, find_p)


def find_p(message):    # search for an object
    url = "https://tarkov-market.com/ru/"
    string = message.text
    try:
        driver.get(url)
        string_input = driver.find_element_by_xpath('//*[@id="__layout"]/div/div/div/div[2]/div[1]/input')
        time.sleep(1)
        string_input.clear()
        string_input.send_keys(string)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        block_things = soup.find(class_="table-list").find_all(class_="row")[1:]

        if len(block_things) == 0:
            bot.send_message(message.chat.id, "product not found")
        else:
            for thing in block_things:      # run through all results
                bot.send_message(message.chat.id, f'Name: {thing.find("a")["title"]}\n'
                                        f'average price for 24 hours, per slot: {thing.find(class_="price-main").text}')

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
