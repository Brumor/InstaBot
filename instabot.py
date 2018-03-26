import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from emoji_support import EmojiFormat
from time import sleep
from collections import OrderedDict
import datetime
import sys


class InstaBot(object):

    def __init__(self, username, password, target_name, isFollow, isLike, isComment, comment1, comment2):
        self.driver = webdriver.Chrome()
        self.username = username
        self.password = password
        self.target_name = target_name
        self.isFollow = isFollow
        self.isLike = isLike
        self.isComment = isComment
        self.comment1 = comment1
        self.comment2 = comment2

    def start(self):

        sys.stdout = open("logs/" + self.username + ".txt", "a")
        print("------------------------------------------------------------------------------------")
        sys.stdout.close()

        self.makeLog("Bot launched ! ")
        self.makeLog("User : " + self.username + ", targeting : " + self.target_name)

        self.login()
        sleep(2)

        if self.verifyElementPresence("slfErrorAlert", 2):
            self.makeLog("Couldn't Login ! Wrong Username/Password or weak connection.")
            return

        # Goes to the competitor's page
        self.driver.get("http://www.instagram.com/" + self.target_name)
        sleep(1)

        #First round with followers
        #usersList = self.getUsersFromFollowers()
        #self.interactWithUsers(usersList)



        # Goes to the competitor's page
        #self.driver.get("http://www.instagram.com/" + self.target_name)
        sleep(1)

        pictureURLs = self.getPictureURLs()

        for i in range(0, len(pictureURLs)):
            self.getPicture(i, pictureURLs)

            sleep(1)

            usersList = self.getUsers()

            self.interactWithUsers(usersList)

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

    def getPicture(self, picture_to_get, urls):

        self.makeLog("Opening picture number " + str(picture_to_get + 1))
        # Opens the first picture
        self.driver.get(urls[picture_to_get - 1])

    def getPictureURLs(self):
        pictureUrls = []

        # Gets all visible pictures
        pictures = self.driver.find_elements_by_class_name("_mck9w")

        # Puts all picture's url in a list
        for picture in pictures:
            pictureUrls.append(picture.find_element_by_tag_name("a").get_attribute("href"))

        self.makeLog("Number of pictures detected : " + str(len(pictureUrls)))

        return pictureUrls

    def getUsers(self):
        users = []

        users1 = self.getUsersFromComments()
        for i in users1:
            users.append(i)

        users2 = self.getUsersFromLikes()
        for i in users2:
            users.append(i)

        self.makeLog("Collected users (" + str(len(users)) + ") = " + str(users))

        return users



    def getUsersFromLikes(self):
        js = '''
            document.querySelector('._nzn1h').click();
        '''

        self.driver.execute_script(js)
        sleep(2)

        js = '''
            a = document.querySelector('._p4iax');
            if (a) {
                a.scrollIntoView({block : "end"});
            }
        '''

        for i in range(0, 20):
            self.driver.execute_script(js)
            sleep(0.7)

        List = self.driver.find_elements_by_class_name("_2nunc")
        users = []
        for i in List:
            elem = i.find_element_by_tag_name("a")
            users.append(elem.get_attribute("title"))

        sleep(20)

        return users

    def getUsersFromComments(self):

        for i in range(100):
            if self.verifyElementPresence("_56pd5", 0):
                js = "document.querySelector('._m3m1c').click(); "
                self.driver.execute_script(js)
            else:
                break

        # Takes every comment and returns a list of URLs and a list of usernames that redirects to active userpage.
        List = self.driver.find_elements_by_class_name("_ezgzd")

        users = []
        for i in List:
            elem = i.find_element_by_tag_name("a")
            users.append(elem.get_attribute("title"))

        # deletes the competitor name
        userToDelete = users[0]
        users = [x for x in users if x != userToDelete]

        # Deletes users that appears more than once !
        users = OrderedDict.fromkeys(users).keys()

        return users

    def getUsersFromFollowers(self):

        js = '''
            var user = arguments[0];
            document.querySelector('a[href="/' + user + '/followers/"]').click();
        '''
        self.driver.execute_script(js, self.target_name)
        sleep(2)

        js = '''
            a = document.querySelector('._8q670');
            a.scrollIntoView({block : "end"});
            
        '''
        for i in range(0,20):
            self.driver.execute_script(js)
            sleep(0.7)

        List = self.driver.find_elements_by_class_name("_2nunc")
        users = []
        for i in List:
            elem = i.find_element_by_tag_name("a")
            users.append(elem.get_attribute("title"))

        self.makeLog("Collected users (" + str(len(users)) +") = " + str(users))

        sleep(20)

        return users


    def interactWithUsers(self, usersList):

        delete_count = 0

        # Goes to every url
        for user in usersList:
            self.driver.get("http://www.instagram.com/" + user)

            # Follow if the follow checkbox has been checked
            if self.isFollow:
                self.makeFollow(user)
                sleep(5)

            if self.verifyElementPresence("_mck9w", 0):

                if self.isLike or self.isComment:

                    # Opens the first picture
                    elem = self.driver.find_element_by_class_name("_mck9w").find_element_by_tag_name("a")
                    self.driver.get(elem.get_attribute("href"))

                    elem = self.driver.find_element_by_tag_name("html")
                    elem.send_keys(Keys.END)

                    # Like if the like checkbox has been checked
                    if self.isLike:
                        self.makeLike(user)

                    # Comment if the comment checkbox has been checked
                    if self.isComment:
                        # Restarts the window after 5 attempts
                        if delete_count % 2 == 0:
                            current_comment = self.comment2
                        else:
                            current_comment = self.comment1

                        self.makeComment(user, current_comment)

                        delete_count = delete_count + 1
                sleep(45)

        self.makeLog("Round finished !")

    def restartWindow(self):
        self.driver.close()
        sleep(5)
        self.driver = webdriver.Chrome()
        sleep(2)
        self.login()
        sleep(1)

    def verifyElementPresence(self, var_name, type_research):

        # 0 : Search by class then "a"
        # 1 : Search by Xpath
        # 2 : search by id
        # 3 : Search by class only

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

    def makeLog(self, message):

        sys.stdout = open("logs/" + self.username + ".txt", "a")
        time = datetime.datetime.now()
        print(str(time.day) + '/' + str(time.month) + '/' + str(time.year) + ', ' + str(time.hour)
              + ':' + str(time.minute) + ':' + str(time.second) + " = " + message.encode("utf-8"))
        sys.stdout.close()

    def makeComment(self, user, comment):

        if self.verifyElementPresence(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/form/textarea', 1):
            sleep(2)
            elem = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/form/textarea')
            elem.click()
            elem = self.driver.find_element_by_class_name("_bilrf")
            elem.clear()
            self.textWithEmojiSupport(comment, elem)
            sleep(0.2)
            elem.send_keys(Keys.RETURN)

            self.makeLog("Commented user's picture : " + user + " with comment '" + comment
                         + "'")

    def makeLike(self, user):

        if self.verifyElementPresence("/html/body/span/section/main/div/div/article/div[2]/section[1]/a[1]/span ", 1) == True:
            js = "document.querySelector('._l9yih').click(); "
            self.driver.execute_script(js)
            self.makeLog("Liked user's picture : " + user)

    def makeFollow(self, user):

        if self.verifyElementPresence("_gexxb", 3) == True:
            js = "document.querySelector('._gexxb').click(); "
            self.driver.execute_script(js)

            self.makeLog("Followed users : " + user)

            time = datetime.datetime.now()
            f = open('followed/' + str(time.day) + '-' + self.username + '.txt', 'a')
            f.write(', ' + user)
            f.close()

    def textWithEmojiSupport(self, text, elem):
        emojisupp = EmojiFormat(text, elem, self.driver)
        emojisupp.detectEmoji()
