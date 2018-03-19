from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

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

JS_ADD_TEXT_TO_INPUT = """
  var elm = arguments[0], txt = arguments[1];
  elm.value += txt;
  elm.dispatchEvent(new Event('change'));
  """

class EmojiFormat:
    def __init__(self, message, elem, driver):
        self.message = message
        self.elem = elem
        self.driver = driver

    def addEmoji(self, keyword):

        if keyword == "thumbs-up":
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, self.elem, thumbs_up)

    def detectEmoji(self):
        message = self.message

        splitted = message.split('/')

        for content in splitted:
            if content[0:2] == "e-":
                self.addEmoji(content[2:])
            else:
                self.elem.send_keys(content)

        self.elem.send_keys(Keys.SPACE)