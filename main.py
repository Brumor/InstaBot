from instabot import InstaBot
from Tkinter import *
import threading

'''
Username henrychinqski1804
Pass : bitcheZ1996

TO-DO:
    ---> test for a day
    ---> write documentation
'''


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

    def run_bot ():
        bot = InstaBot(usr, psswrd, trgt, fllw, lk, cmmnt,
                       cmmnt1, cmmnt2)
        bot.start()
    threading.Thread(target=run_bot).start()

username.grid(row=0, column=1)
password.grid(row=1, column=1)
target_username.grid(row=2, column=1)
comment1.grid(row=6, column=1)
comment2.grid(row=7, column=1)

Button(master, text='Start', command=start).grid(row=8, column=1, sticky=W)

for child in master.winfo_children():
    child.grid_configure(padx=20, pady=10)

mainloop()
