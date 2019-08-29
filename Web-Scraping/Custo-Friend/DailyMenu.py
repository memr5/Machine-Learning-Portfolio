# Importing required Libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from selenium import webdriver                                     # Selenium is to do automated tasks on browser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Url of the website
url = 'https://www.custofriend.com/pdpu-mess-menu/'

# To make a request to the website 
request = requests.get(url)

# To create a BeautifulSoup object with content(Source code) of the website
soup = BeautifulSoup(request.content,'html5lib')

# Dictionary to store food iteams
Meals = {"BREAKFAST":[],
        "LUNCH":[],
        "SNACKS":[],
        "DINNER":[]}


def fetchMenu():

    # Fetching required content from the source-code for fetching food items
    meals = soup.find('div',attrs={'class':'vc_row wpb_row vc_row-fluid vc_custom_1534879168928 vc_row-has-fill'})
    #print(meals.prettify())

    # Iterating over many results from 'meals' to to fetch content meal wise (ex:Breakfast,Lunch etc)
    for meal in meals.find_all('div',attrs={'class':'wpb_wrapper'}):

        #print(meal.strong.text)
        meal_name = meal.strong.text
        
        # Only filling dictionary one time for specified meal as results fetched are duplicated twice
        if meal_name in ["BREAKFAST","LUNCH","SNACKS","DINNER"] and len(Meals[meal_name]) == 0:

            for item in meal.find_all('span',attrs={'style':'color: #329af5;'}):
                #print(item.text.strip())
                Meals[meal_name].append(item.text.strip())

        # Breaking the loop after fetching items in Dinner
        if meal_name == "DINNER":
            break


def dateCheck():
    # Today's date
    global todayDate 
    todayDate = datetime.datetime.now().strftime("%d/%m/%y")
    #print(todayDate)

    # Date on website
    date = soup.find('span',attrs={'style':'color: #ff0000;'}).text.split(' ')[2]
    date = date.split('/')
    menuDate = datetime.datetime(2000+int(date[2],10),int(date[1],10),int(date[0],10)).strftime("%d/%m/%y")
    #print(menuDate)

    # Comparing both dates to check if menu is updated or not
    if todayDate != menuDate:
        return 1
    else:
        return 0


# To set proper message format to send it on whatsapp
def setMessageFormat():
    global formattedMessage

    formattedMessage = "----------------------------"
    formattedMessage += "\nDate : *{}*\n\n*MENU*".format(todayDate)

    for meal in Meals:
        formattedMessage += "\n\n*" + str(meal) + "*\n"
        for items in Meals[str(meal)]:
            formattedMessage += "\n" + str(items)

    formattedMessage += "\n\n----------------------------"


# To send menu on Whatsapp
def sendMenu():

    print("Sending.....")

    driver = webdriver.Chrome('chromedriver')
    driver.get('https://web.whatsapp.com/')

    # Name to the user 
    userName = "Memr5"

    input("\nPress anything after scanning QR-code!!")

    # To find user from recent chat (it will not work if user is not in recent chat list)
    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(userName))
    user.click()

    # To find message box
    messageBox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    setMessageFormat()
    
    # To send message
    for ch in formattedMessage:
        if ch == "\n":
            # To go to new line in the message
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
        else:
            messageBox.send_keys(ch)
    # To send entire message after pushing it in the message box
    messageBox.send_keys(Keys.ENTER)
    time.sleep(10)


def main():
    if dateCheck()!=1 :
        fetchMenu()
        sendMenu()
    else:
        print("Menu not updated on website!")


main()