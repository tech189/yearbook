from selenium import webdriver
import time
from bs4 import BeautifulSoup
import mysql.connector
import os

def insertData(person_name, person_house, person_nicknames, person_email, person_birthday, person_subjects):
    person_name = person_name.replace("'", "\\'")
    person_house = person_house.replace("'", "\\'")
    '''
    #This can be used later to unescape the "\'"
    bks = bks.replace("\\'", "'")
    print(bks)
    bks = ast.literal_eval(bks)
    i = 0
    print("\nRelated books:")
    while (i < len(bks.keys())):
        print(list(bks.keys())[i] + " : " + bks[list(bks.keys())[i]])
        i = i + 1
    '''

    connection = mysql.connector.connect(user="root", password="", host="localhost", database="yearbook")
    cursor = connection.cursor()

    
    cursor.execute("INSERT INTO people (person_name, person_house, person_nicknames, person_email, person_birthday, person_subjects) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" %(person_name, person_house, person_nicknames, person_email, person_birthday, person_subjects))
    connection.commit()

    print("Added to people table")

    cursor.close()
    connection.close()

def readDatabase():
    connection = mysql.connector.connect(user="root", password="", host="localhost", database="yearbook")
    cursor = connection.cursor()
    cursor.execute("SELECT person_id, person_name, person_house, person_nicknames, person_email, person_birthday, person_subjects, date_added FROM people")
    row = cursor.fetchone()

    if row is None:
        print("Empty people table")
    while row is not None:
        print(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        row = cursor.fetchone()

    cursor.close()
    connection.close()

def getData():
    browser = webdriver.Firefox()
    browser.get("http://yearbook.com/login")

    username = browser.find_element_by_id("username")
    password = browser.find_element_by_id("password")
    login = browser.find_element_by_xpath("//button[contains(.,'login')]")

    input1 = input("Username: ")
    input2 = input("Password: ")
    username.send_keys(input1)
    password.send_keys(input2)

    login.click()

    time.sleep(3)

    browser.get("https://yearbook.com/s/people/list")
    
    time.sleep(2)

    html_soup = BeautifulSoup(browser.page_source,'html.parser')

    people = html_soup.find_all("li", attrs={"class": "user"})

    counter = 1
    link_dict = {}
    original_dir = os.getcwd()
    if not os.path.exists("Screenshots"):
            os.makedirs("Screenshots")
    os.chdir("Screenshots")

    for i in people:
        print("Person " + str(counter))
        counter += 1

        name = i.find("a", attrs={"class": "userInfo--primary"}).get_text()
        print("Name: " + name)

        house = i.find("span", attrs={"class": "userInfo--secondary"}).get_text()
        print("House: " + house)

        link = "http://yearbook.com" + i.find("a", attrs={"class": "userInfo--primary"})['href']
        print("Link: " + link)

        link_dict[name] = link

        browser.get(link)
        time.sleep(5)
        browser.get_screenshot_as_file(name + ".png")
        '''
        person_soup = BeautifulSoup(browser.page_source, "html.parser")
        details = person_soup.find_all("div", attrs={"class": "profile-detail-value"})
        print("Details: " + str(details))
        
        counter2 = 1
        for i in details:
            if counter2 == 1:
                nicknames = i.get_text()
                print("Nickname(s): " + nicknames)
                counter2 += 1
            elif counter2 == 2:
                email = i.get_text()
                print("Email: " + email)
                counter2 += 1
            elif counter2 == 3:
                birthday = i.get_text()
                print("Birthday: " + birthday)
                counter2 += 1
            elif counter2 == 4:
                subjects = i.get_text()
                print("Subjects: " + subjects)
                counter2 += 1
        counter2 = 1

        #inserts the data into the MySQL database, disabled for testing
        #insertData(name, house, nicknames, email, birthday, subjects)

        friends_say = person_soup.find_all("textarea")
        print(str(friends_say))
        
        for i in friends_say:
            print(str(i.get_text()))
        '''
        os.chdir(original_dir)

        if not os.path.exists("Pages"):
            os.makedirs("Pages")

        with open(os.getcwd() + "\\" + os.path.join("Pages", name) + ".html", mode="w") as page:
            html_not_encoded = browser.page_source
            html_encoded = html_not_encoded.encode("utf8")
            page.write(str(html_encoded))

        #stops after 10 people for testing
        #if counter > 10:
        #   break

    #will quit the browser after scraping, disabled for testing
    #browser.quit()

readDatabase()
getData()