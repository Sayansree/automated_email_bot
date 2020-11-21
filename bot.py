import smtplib
import re
import sys
import getpass
import random
import math
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header    import Header
import socket 
socket.setdefaulttimeout(10)
path=os.path.dirname(os.path.realpath(__file__))
""" 
created by sayansree paria
verson<1.0>

"""
print("\n\n\n\temail bot v1.0\n\tdevlovper sayansree paria\n\n ")

def check(email):
    if not re.match(r"[\w\.-_]+@[\w]+\.com",email):
        print(email + '\t is invalid email id format\n')
        return False
    else:
        return True
def loadBotEmail():
    try:
        file=open(path+'/bot.txt','r')
        lines=file.readlines()
        if not check(lines[0].split('|')[0]) :
            sys.exit(0)
    except FileNotFoundError:
        print ("please define bot.txt")
        #raise 
        sys.exit(0)
    except:
        print("unexpected fatal error encountered while accessing bot.txt\nmake sure code has access permition")
        #raise
        sys.exit(0)
    else:
        print ("\tbot email successfully imported")
        file.close()
        return (lines[0].split('|')[0],lines[0].split('|')[1])
def now():
    return time.localtime().tm_hour*60+time.localtime().tm_min
def loadTargets():
    targetList=[]
    try:
        file=open(path+'/target.txt','r')
        lines=file.readlines()
        targets=[]
        tm=lines[0][1:-1]
        for i in lines[1:]:
            if i[0] is '#':
                if len(targets)>0 :
                    targetList.append([tm,targets])
                tm=i[1:-1]
                targets=[]
            else:
                if check(i.split('|')[0]) :
                    targets.append(i.split('|'))
        del lines
        targetList.append([tm,targets])
    except FileNotFoundError:
        print ("please define target.txt")
        sys.exit(0)
    except:
        print("unexpected fatal error encountered while accessing target.txt\nmake sure code has access permition")
        sys.exit(0)
    else:
        print ("\ttarget emails successfully imported")
        file.close()
    return targetList
def connect():
    try:
        server =smtplib.SMTP_SSL('smtp.gmail.com',465)
    except :
        print('\ncheck your internet connection')
        sys.exit(0)
    else:
        print('\n\t\t\tconnection established')
    return server
def authenticate(server,bot):  
    sender=bot[0]
    password=bot[1]
    try:
        server.login(sender,password)
    except smtplib.SMTPConnectError:
        print('\nconnection error') 
        server.quit()    
    except smtplib.SMTPAuthenticationError:
        print('\nauthentication failed: '+sender+"\t"+'*'*5+password[-3:])
        server.quit()     
    except:
        print('\nunexpected error') 
        server.quit()
        raise
    else:
        print('\tsuccesfully authenticated\t'+sender)
def mail(server,target,sender):
    msg= MIMEMultipart()
    msg['From'] = sender
    msg['To']=  target[0]
    msg['Subject']= target[1]
    msg.attach(MIMEText(target[2],'html'))
    server.sendmail(msg['From'],msg['To'],msg.as_string())
    del msg
    print('<{0}...> mailed to {1}'.format(target[1],target[0]))   
    time.sleep(0.1) 
def findSlots(userId):
    i=userId[0][0]
    m=int(i.split(':')[0])*60+int(i.split(':')[1])
    for timeslot in userId:
        slot=int(timeslot[0].split(':')[0])*60+int(timeslot[0].split(':')[1])
        if now() >=slot:
            return timeslot
        m=min(slot,m)
    return m
def processTimeslot(timeslot,server,email):
    slot=timeslot[0]
    targets=timeslot[1]
    print("processing timeslot {0} with {1} targets".format(slot,len(targets)))
    for target in targets:
        mail(server,target,email[0])
def launch(timeout):
    userId=loadTargets()
    email=loadBotEmail()
    server=connect()
    authenticate(server,email)
    print('\n\ttimeslots execution started\n\n')
    while(now()<timeout and len(userId) > 0):
        print("\nfinding timeslots..")
        timeslot=findSlots(userId)
        if type(timeslot) is int:
            print("next timeslot in {0}:{1}".format(timeslot//60,timeslot%60))
            time.sleep((timeslot-now())*60)
        else:
            processTimeslot(timeslot,server,email)
            userId.remove(timeslot)
    print('\t terminating server connections')
    server.quit()
    
timeout=int(input("enter runtime for bot server in minutes:"))
timeout+=now()
launch(timeout)