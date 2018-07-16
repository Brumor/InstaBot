# coding=utf-8
from tkinter import *
import threading
from unfollower import Unfollower
from selenium.webdriver.common.keys import Keys
from emoji_support import EmojiFormat
from collections import OrderedDict
import os
import datetime
from selenium import webdriver
from time import sleep
import sys

#see https://apps.timwhitlock.info/emoji/tables/unicode for a list of every emoji

# Emoji Support D83D DC9C
red_heart = u'\u2764'
blue_heart = u'\ud83d\udc99'
green_heart = u'\ud83d\udc9a'
yellow_heart = u'\ud83d\udc9b'
purple_heart = u'\ud83d\udc9c'
orange_heart = u'\ud83e\udde1'
heart_exclamation = u"\u2763"

smiling_face = u'\ud83d\ude0a'
heart_face = u'\ud83d\ude0d'
hug_face = u'\ud83e\udd17'

okay_hand = u'\ud83d\udc4c'
thumbs_up = u'\ud83d\udc4d'
left_fist = u'\ud83e\udd1b'

fire = u'\ud83d\udd25'
top_sign = u'\ud83d\udd1d'
cat = u'\ud83d\udc31'
eyes = u'\ud83d\udc40'
crown = u'\ud83d\udc51'

#JS To add Emojis
JS_ADD_TEXT_TO_INPUT = """
  var elm = arguments[0], txt = arguments[1];
  elm.value += txt;
  elm.dispatchEvent(new Event('change'));
  """

#Codes for button and HTML elements
usernameElem = "username"
passwordElem = "password"
loginBtnElem = "_5f5mN"
followersFrameJSElem = "._1xe_U"
userElem = "FsskP"
pictureElem = "v1Nh3"
commentElem = "gElp9"
loadCommentsElem = "vTJ4h"
likesElem = "zV_Nj"
likesButtonElem = "coreSpriteHeartOpen"
followButtonElem = "_6VtSN"
commentTextAreaElem = "Ypffh"

class EmojiFormat:
    def __init__(self, message, elem, driver):
        self.message = message
        self.elem = elem
        self.driver = driver

    def addEmoji(self, keyword):

        if keyword == "red_heart":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, red_heart)
        elif keyword == "blue_heart":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, blue_heart)
        elif keyword == "green_heart":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, green_heart)
        elif keyword == "yellow_heart":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, yellow_heart)
        elif keyword == "purple_heart":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, purple_heart)
        elif keyword == "orange_heart":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, orange_heart)
        elif keyword == "heart_exclamation":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, heart_exclamation)
        elif keyword == "smiling_face":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, smiling_face)
        elif keyword == "heart_face":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, heart_face)
        elif keyword == "hug_face":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, hug_face)
        elif keyword == "okay_hand":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, okay_hand)
        elif keyword == "thumbs_up":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, thumbs_up)
        elif keyword == "left_fist":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, left_fist)
        elif keyword == "fire":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, fire)
        elif keyword == "top_sign":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, top_sign)
        elif keyword == "cat":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, cat)
        elif keyword == "eyes":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, eyes)
        elif keyword == "crown":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, crown)


    def detectEmoji(self):
        message = self.message

        splitted = message.split(' ')
        for content in splitted:
            if content[0:3] == "/e-":
                self.addEmoji(content[3:])
            else:
                self.elem.send_keys(content)
                self.elem.send_keys(Keys.SPACE)

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

        sys.stdout = open("logs/" + self.username + ".txt", "w")
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

        usersList = self.getUsers()

        self.interactWithUsers(usersList)

    def login(self):
        self.makeLog("Log in...")
        # Open Login Page
        self.driver.get("http://www.instagram.com/accounts/login")
        sleep(2)

        # enters login
        elem = self.driver.find_element_by_name(usernameElem)
        elem.clear()
        elem.send_keys(self.username)

        # enters password
        elem = self.driver.find_element_by_name(passwordElem)
        elem.clear()
        elem.send_keys(self.password)

        sleep(2)

        # Clicks the login button and waits fo the page to load
        elem = self.driver.find_element_by_class_name(loginBtnElem)
        elem.click()

    def getPicture(self, picture_to_get, urls):

        self.makeLog("Opening picture number " + str(picture_to_get + 1))
        # Opens the first picture
        self.driver.get(urls[picture_to_get])

    def getPictureURLs(self):
        pictureUrls = []

        # Gets all visible pictures
        pictures = self.driver.find_elements_by_class_name(pictureElem)

        # Puts all picture's url in a list
        for picture in pictures:
            pictureUrls.append(picture.find_element_by_tag_name("a").get_attribute("href"))

        self.makeLog("Number of pictures detected : " + str(len(pictureUrls)))

        return pictureUrls

    def getUsers(self):
        users = []

        # First round with followers
        usersFollowed = self.getUsersFromFollowers()

        for i in usersFollowed:
            users.append(i)

        pictureURLs = self.getPictureURLs()

        # Second round with user liking and commenting on pictures
        for i in range(0, len(pictureURLs)):
            self.getPicture(i, pictureURLs)

            sleep(1)

            # Gets users from the comments under the picture
            usersComments = self.getUsersFromComments()
            for i in usersComments:
                users.append(i)

            # Gets users from the Likes under the picture
            if (self.verifyElementPresence(likesElem, 3)):
                usersLikes = self.getUsersFromLikes()
                for i in usersLikes:
                    users.append(i)

        # Deletes users that appears more than once !
        users = OrderedDict.fromkeys(users).keys()

        self.makeLog("Collected users = " + str(len(users)))

        return users

    def getUsersFromLikes(self):
        js = "document.querySelector('." +likesElem + "').click();"


        self.driver.execute_script(js)
        sleep(2)

        js = '''
            a = document.querySelector(arguments[0]);
            if (a) {
                a.scrollIntoView({block : "end"});
            }
        '''

        for i in range(0, 4):
            self.driver.execute_script(js, followersFrameJSElem)
            sleep(1)

        List = self.driver.find_elements_by_class_name(userElem)
        users = []
        for i in List:
            elem = i.find_element_by_tag_name("a")
            users.append(elem.get_attribute("title"))

        sleep(2)

        return users

    def getUsersFromComments(self):

        for i in range(20):
            if self.verifyElementPresence(loadCommentsElem, 0):
                js = "document.querySelector('." + loadCommentsElem + "').click();"
                self.driver.execute_script(js)
                sleep(1)
            else:
                break

        # Takes every comment and returns a list of URLs and a list of usernames that redirects to active userpage.
        List = self.driver.find_elements_by_class_name(commentElem)

        users = []
        for i in List:
            elem = i.find_element_by_tag_name("a")
            users.append(elem.get_attribute("title"))

        # deletes the competitor name
        userToDelete = users[0]
        users = [x for x in users if x != userToDelete]

        return users

    def getUsersFromFollowers(self):

        js = '''
            var user = arguments[0];
            document.querySelector('a[href="/' + user + '/followers/"]').click();
        '''
        self.driver.execute_script(js, self.target_name)
        sleep(2)

        js = '''
            a = document.querySelector(arguments[0]);
            a.scrollIntoView({block : "end"});
        '''
        for i in range(0, 4):
            self.driver.execute_script(js, followersFrameJSElem)
            sleep(1)

        List = self.driver.find_elements_by_class_name(userElem)
        users = []
        for i in List:
            elem = i.find_element_by_tag_name("a")
            users.append(elem.get_attribute("title"))

        sleep(2)

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

            if self.verifyElementPresence(pictureElem, 0):

                if self.isLike or self.isComment:

                    # Opens the first picture
                    elem = self.driver.find_element_by_class_name(pictureElem).find_element_by_tag_name("a")
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
                sleep(5)

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
        msg = str(time.day) + '/' + str(time.month) + '/' + str(time.year) + ', ' + str(time.hour) + ':' + str(
            time.minute) + ':' + str(time.second) + " = " + message
        print(bytes(msg.encode("utf-8")).decode("utf-8"))
        sys.stdout.close()

    def makeComment(self, user, comment):

        if self.verifyElementPresence(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/form/textarea', 1):
            sleep(2)
            elem = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/form/textarea')
            elem.click()
            elem = self.driver.find_element_by_class_name(commentTextAreaElem)
            elem.clear()
            self.textWithEmojiSupport(comment, elem)
            sleep(0.2)
            elem.send_keys(Keys.RETURN)

            self.makeLog("Commented user's picture : " + user + " with comment '" + comment
                         + "'")

    def makeLike(self, user):

        if self.verifyElementPresence("coreSpriteHeartOpen", 3) == True:
            js = "document.querySelector('." + likesButtonElem +"').click(); "
            self.driver.execute_script(js)
            self.makeLog("Liked user's picture : " + user)

    def makeFollow(self, user):

        if self.verifyElementPresence(followButtonElem, 3) == True:
            js = "document.querySelector('." + followButtonElem + "').click(); "
            self.driver.execute_script(js)

            self.makeLog("Followed users : " + user)

            time = datetime.datetime.now()
            f = open('followed/' + str(time.day) + '-' + self.username + '.txt', 'a')
            f.write(', ' + user)
            f.close()

    def textWithEmojiSupport(self, text, elem):
        emojisupp = EmojiFormat(text, elem, self.driver)
        emojisupp.detectEmoji()

class Unfollower(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logs = 'logs/'

    def start(self):
        sleep(20)
        self.makeLog("Unfollower Bot launched ! ")


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
            sleep(300)

    def login(self):
        self.makeLog("Log in...")
        # Open Login Page
        self.driver.get("http://www.instagram.com/accounts/login")
        sleep(2)

        # enters login
        elem = self.driver.find_element_by_name(usernameElem)
        elem.clear()
        elem.send_keys(self.username)

        # enters password
        elem = self.driver.find_element_by_name(passwordElem)
        elem.clear()
        elem.send_keys(self.password)

        sleep(2)

        # Clicks the login button and waits fo the page to load
        elem = self.driver.find_element_by_class_name(loginBtnElem)
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
            if i[0:2] == str(self.now.day):

                if i[3:-4] == self.username:
                    f = open(dir + i, 'r')
                    a = f.read()
                    f.close()
                    usrs = a.split(", ")

                    # deletes the first blank space
                    usrs = usrs[1:]
                    break

            elif i[0:1] == str(self.now.day):
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

        self.driver.get("http://www.instagram.com/" + user)

        if self.verifyElementPresence(followButtonElem, 3):
            self.makeLog(user)

            js = "document.querySelector('."+ followButtonElem + "').click(); "
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

master = Tk()
master.title("Insta Bot")

username = Entry(master)
password = Entry(master, show="*")
target_username = Entry(master)
comment1 = Entry(master)
comment2 = Entry(master)

Label(master, text="Username :").grid(row=0)
Label(master, text="Password :").grid(row=1)
Label(master, text="Target @ :").grid(row=2)
Label(master, text="Message 1 :").grid(row=6)
Label(master, text="Message 2 :").grid(row=7)

follow = BooleanVar()
Checkbutton(master, text="Follow :", variable=follow).grid(row=3, sticky=W)
like = BooleanVar()
Checkbutton(master, text="Like :", variable=like).grid(row=4, sticky=W)
comment = BooleanVar()
Checkbutton(master, text="Comment :", variable=comment).grid(row=5, sticky=W)


def start():
    usr = username.get()
    psswrd = password.get()
    trgt = target_username.get()
    fllw = follow.get()
    lk = like.get()
    cmmnt = comment.get()
    cmmnt1 = comment1.get()
    cmmnt2 = comment2.get()

    def run_bot():
        bot = InstaBot(usr, psswrd, trgt, fllw, lk, cmmnt,
                       cmmnt1, cmmnt2)
        bot.start()

    def run_unfollow():
        unfollowbot = Unfollower(usr, psswrd)
        unfollowbot.start()

    threading.Thread(target=run_bot).start()

    if fllw == True:
        threading.Thread(target=run_unfollow).start()

    return


username.grid(row=0, column=1)
password.grid(row=1, column=1)
target_username.grid(row=2, column=1)
comment1.grid(row=6, column=1)
comment2.grid(row=7, column=1)

username.insert(0, "")
password.insert(0, "")

Button(master, text='Start', command=start).grid(row=8, column=1, sticky=W)

for child in master.winfo_children():
    child.grid_configure(padx=20, pady=10)

mainloop()
