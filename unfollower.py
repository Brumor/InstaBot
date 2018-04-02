import os
import datetime
from selenium import webdriver
from time import sleep
import sys



class Unfollower(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logs = 'logs/'

    def start(self):
        self.makeLog("Unfollower Bot launched ! ")
        sleep(2)


        while True:
            self.now = datetime.datetime.now()

            usrs = self.openFollowedTxt()

            if(usrs != None):
                self.driver = webdriver.Chrome()
                self.login()
                sleep(2)

                if self.verifyElementPresence("slfErrorAlert", 2):
                    self.makeLog("Couldn't Login ! Wrong Username/Password or weak connection.")
                    return

                for i in range(0, len(usrs)):
                    self.unfollowUser(usrs[i])
                    sleep(2)

                fileToDelete = "followed/" + str(self.now.day) + '-' + self.username + '.txt'
                os.remove(fileToDelete) # remove file
                self.driver.close()
            else:
                self.makeLog("Waiting for more files...")
            sleep(43200)

    def login(self):
        self.makeLog("Log in...")
        # Open Login Page
        self.driver.get("http://www.instagram.com/accounts/login")
        sleep(2)

        # enters login
        elem = self.driver.find_element_by_name("username")
        elem.clear()
        elem.send_keys(self.username)

        # enters password
        elem = self.driver.find_element_by_name("password")
        elem.clear()
        elem.send_keys(self.password)

        sleep(2)

        # Clicks the login button and waits fo the page to load
        elem = self.driver.find_element_by_class_name("_gexxb")
        elem.click()

    def formateDateDifference(value, time):
        if value <= 0:
            if time.month == 5 or time.month == 7 or time.month == 10 or time.month == 12:
                return 30 + value
            elif time.month == 3:
                return 28 + value
            else:
                return 31 + value
        else:
            return value

    def openFollowedTxt(self):
        dir = 'followed/'
        files = os.listdir(dir)

        usrs = None

        for i in files:
            if i[0:2] == str(self.now.day - 2):

                if i[3:-4] == self.username:
                    f = open(dir + i, 'r')
                    a = f.read()
                    f.close()
                    usrs = a.split(", ")

                    # deletes the first blank space
                    usrs = usrs[1:]
                    break

            elif i[0:1] == str(self.now.day - 2):
                if i[3:-4] == self.username:
                    f = open(dir + i, 'r')
                    a = f.read()
                    f.close()

                    usrs = a.split(", ")

                    # deletes the first blank space
                    usrs = usrs[1:]
                    break
            else:
                usrs =  None

        self.makeLog(str(usrs))

        return usrs

    def makeLog(self, message):
        sys.stdout = open(self.logs + self.username + ".txt", "a")
        time = datetime.datetime.now()
        msg = str(time.day) + '/' + str(time.month) + '/' + str(time.year) + ', ' + str(time.hour) + ':' + str(
            time.minute) + ':' + str(time.second) + " = " + message
        print(bytes(msg.encode("utf-8")).decode("utf-8"))
        sys.stdout.close()

    def unfollowUser(self, user):
        #_qv64e

        self.driver.get("http://www.instagram.com/" + user)

        if self.verifyElementPresence("_t78yp", 3):
            self.makeLog(user)

            js = "document.querySelector('._t78yp').click(); "
            self.driver.execute_script(js)

    def verifyElementPresence(self, var_name, type_research):

        #0 : Search by class then "a"
        #1 : Search by Xpath
        #2 : search by id
        #3 : Search by class only

        if type_research == 0:
            try:
                self.driver.find_element_by_class_name(var_name).find_element_by_tag_name("a")
            except:
                return False
            return True

        elif type_research == 1:
            try:
                self.driver.find_element_by_xpath(var_name)
            except:
                return False
            return True
        elif type_research == 2:
            try:
                self.driver.find_element_by_id(var_name)
            except:
                return False
            return True
        elif type_research == 3:
            try:
                self.driver.find_element_by_class_name(var_name)
            except:
                return False
            return True
        else:
            return False

if __name__ == "__main__":
    unfollow = Unfollower("henrychinqski1804", "bitcheZ1996")
    unfollow.start()