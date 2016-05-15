#!/usr/bin/env python

#Daniel Marin
#03/09/2015
#This program gets profiles from interpals.net and responds to them automatically

import time
import sys
import os
import requests
from requests.adapters import HTTPAdapter
import re
import random
import getpass
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cleverbot'))
#import cleverbot.py
import cleverbot.py

mindelay = 1
maxdelay = 5
sex = '' # Possible values: 'male', 'female', or '' for both
cont = 'NA AS EU OC SA' #continent
age1 = 18 # minimum age
age2 = 38 # maximum age

visitedUsersFilename = "users_visited.txt" #Visited Users
openthreads="openthreads.txt" #Current convos
datafile="myData.txt" #Sender's info

#Social media
skype="n/a"
kakaotalk="n/a"
whatsapp="n/a"
snapchat="n/a"
viber="n/a"
telegram="n/a"
facebook="n/a"
kik="n/a"
phone="n/a"
email1="n/a"
address="n/a"

#Info variables
myname="n/a"
myplace="n/a"
myage="n/a"
mynativelang="n/a"
mylearninglang="n/a"

#Lists of users and threads
processedUsers=""
threads=""

#Checks if file is empty, stolen from stackexchange
def is_non_zero_file(fpath):  
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False

# # # # #REAL CODE BEGINS# # # # #

sessioncount=0
run_number = 1
f = open(datafile, 'a+')
mydata = [line.strip() for line in f]
s = requests.Session()

#Info file I/O
if is_non_zero_file(datafile):
	login=mydata [0]
	password=mydata [1]

	myname=mydata [2]
	myplace=mydata [3]
	myage=mydata [4]
	mynativelang=mydata [5]
	mylearinglang=mydata [6]

	skype=mydata [7]
	kakaotalk=mydata [8]
	whatsapp=mydata [9]
	snapchat=mydata [10]
	viber=mydata [11]
	telegram=mydata [12]
	facebook=mydata [13]
	kik=mydata [14]
	phone=mydata [15]
	email1=mydata [16]
	address=mydata [17]
else:
	login = raw_input('Username (mail): ')
	password = getpass.getpass('Password: ')
	myname = raw_input('Your name: ')
	myplace = raw_input('Your city, country: ')
	myage = raw_input('Your age: ')
	mynativelang = raw_input('Your native language: ')
	print "Enter the accounts of any of the following that you have."
	mylearninglang = raw_input('The primary language you\'re learning: ')
	skype = raw_input('Skype: ')
	kakaotalk = raw_input('Kakaotalk: ')
	whatsapp = raw_input('Whatsapp: ')
	snapchat = raw_input('Snapchat: ')
	viber = raw_input('Viber: ')
	telegram = raw_input('Telegram: ')
	facebook = raw_input('Facebook: ')
	kik = raw_input('Kik: ')
	phone = raw_input('Phone #: ')
	email1 = raw_input('Email address: ')
	address = raw_input('Home address: ')
	save = raw_input('Save info? [Y/N]: ')
	if save=="Y":
		f.write(login + "\n")
		f.write(password + "\n")
		f.write(myname + "\n")
		f.write(myplace + "\n")
		f.write(myage + "\n")
		f.write(mynativelang + "\n")
		if mylearninglang:
			f.write(mylearninglang + "\n")
		else:
			f.write("n/a\n")
		if skype:
			f.write(skype + "\n")
		else:
			f.write("n/a\n")
		if kakaotalk:
			f.write(kakaotalk + "\n")
		else:
			f.write("n/a\n")
		if whatsapp:
			f.write(whatsapp + "\n")
		else:
			f.write("n/a\n")
		if snapchat:
			f.write(snapchat + "\n")
		else:
			f.write("n/a\n")
		if viber:
			f.write(viber + "\n")
		else:
			f.write("n/a\n")
		if telegram:
			f.write(telegram + "\n")
		else:
			f.write("n/a\n")
		if facebook:
			f.write(facebook + "\n")
		else:
			f.write("n/a\n")
		if kik:
			f.write(kik + "\n")
		else:
			f.write("n/a\n")
		if phone:
			f.write(phone + "\n")
		else:
			f.write("n/a\n")
		if email1:
			f.write(email1 + "\n")
		else:
			f.write("n/a\n")
		if address:
			f.write(address + "\n")
		else:
			f.write("n/a\n")
		f.close()

#Login and intro message
payload = {'action': 'login', 'login': login, 'auto_login' : '0', 'password': password}
s.get("http://www.interpals.net/")
r = s.post("http://www.interpals.net/login.php", data=payload)
print "Use keywords like {name}, {country}, {city}, {age}, {user}, and {gender}"
msgGet = raw_input('Enter an intro message: ')

## THE L O O P ##

while True:
	d = open(visitedUsersFilename, 'a+')
	processedUsers = [line.strip() for line in d]
	g = open(openthreads, 'a+')
	threads= [line.strip() for line in g]
	runcount=0
	r = s.get("http://www.interpals.net/online.php?sex=%s&cont=%s&age1=%d&age2=%d" % (sex, cont, age1, age2))
	data = r.text
	usernames = re.findall(r'<div class=\'online_prof\'><a href=\'([a-zA-Z0-9\-_]+)\'', data, re.M)
	for username in usernames:
		if username not in processedUsers:

			#Views users, sends intro message and gets threadid
			runcount += 1
			sessioncount += 1
			r = s.get("http://www.interpals.net/" + username)
			data=r.text
			uids =re.findall(r'uid=([0-9]+)', data, re.M)
			uid= uids[0]
			gender2=re.findall(r'(f?e?male)-14.png', data, re.M) [0]
			country2 =re.findall(r'<a href=\'country/..\'>([A-Za-z ]+)</a>', data, re.M) [0]
			city2 =re.findall(r'city=[0-9]+\'>([^&]+)</a>,', data, re.M)[0].encode('utf-8')
			age2 =re.findall(r'(..) y\.o\.', data, re.M) [0]
			names2=re.findall(r'</h1> (.+), .. y\.o\.', data, re.M)
			name2=""
			if not names2:
				name2=username
			else:
				name2=names2[0].encode('utf-8')
			r=s.get("http://www.interpals.net/pm.php?action=send&uid="+uid)
			data=r.text
			threadids = re.findall(r'thread_id=([0-9]+)', data, re.M)
			threadid=""
			if threadids:
				threadid=threadids[0]
				msg= msgGet.format(user=username, gender=gender2, country=country2, city=city2, age=age2, name=name2)
				payload = {'action': 'send_message', 'thread': threadid, 'message': msg}
			r=s.post("http://www.interpals.net/pm.php?thread_id="+threadid, data=payload)
			waitTime = random.randrange(mindelay, maxdelay)
			os.system('cls' if os.name=='nt' else 'clear')
			print ('\rRun %d - Responded to %d users (%d new)' % (run_number, runcount, sessioncount))
			time.sleep(waitTime)
			processedUsers.append(username)
			d.write(username + "\n")
			threads.append(threadid)
			g.write(threadid+"\n")

		# # # AI # # #
		for threadid in threads:
			s.mount("http://www.interpals.net/pm.php?thread_id="+threadid, HTTPAdapter(max_retries=99))
			r=s.get("http://www.interpals.net/pm.php?thread_id="+threadid)
			data=r.text
			replies=re.findall(r'moderators"></i>\n((?!msg_body).)*\n</div>\n<div class="msg_body">(((?!msg_body)(?s).)+)</div>\n</div>\n<div class="msg_last_online', data, re.M)
			if replies:
				runcount += 1
				reply1=replies [0]
				replies2=re.split(r'(<br/>\n)|(\.)+|(\!)+|(\?)+', reply1[1])
				while ("" in replies2):
					replies2.remove("")
				while (None in replies2):
					replies2.remove(None)
				while ("." in replies2):
					replies2.remove(".")
				while ("!" in replies2):
					replies2.remove("!")
				while ("?" in replies2):
					replies2.remove("?")
				while ("<br/>\n" in replies2):
					replies2.remove("<br/>\n")
				while (" " in replies2):
					replies2.remove(" ")
				if not replies2:
					replies2="?"
				cb1=cleverbot.Cleverbot()
				for reply3 in replies2:
					reply=reply3.lower()
					botrep=""

					#Get botresponse, filter incorrect responses
					if ("what" in reply) and ("name" in reply):
						botrep=botrep+"My facebook is "+myname+". "
					if ("where" in reply) and (("u live" in reply) or ("from" in reply)):
						botrep=botrep+"I live in "+myplace+". "
					if ("what" in reply) and ("age" in reply):
						botrep=botrep+"I am "+myage+" years old. "
					if ("what" in reply) and ("language" in reply) and (("u speak" in reply) or ("native" in reply)):
						botrep=botrep+"My native language is "+mynativelang+". "
					if ("what" in reply) and ("language" in reply) and ("learn" in reply) and (mylearninglang != "n/a"):
						botrep=botrep+"I'm learning "+mylearninglang+". "
					if (botrep==""):
						botrep=botrep+"Add me! "
					if ("skype" in reply) and (skype != "n/a"):
						botrep=botrep+"My skype is "+skype+". "
					if ("kakaotalk" in reply) and (kakaotalk != "n/a"):
						botrep=botrep+"My kakaotalk is "+kakaotalk+". "
					if ("whatsapp" in reply) and (whatsapp != "n/a"):
						botrep=botrep+"My whatsapp is "+whatsapp+". "
					if ("snapchat" in reply) and (snapchat != "n/a"):
						botrep=botrep+"My snapchat is "+snapchat+". "
					if ("viber" in reply) and (viber != "n/a"):
						botrep=botrep+"My viber is "+viber+". "
					if ("telegram" in reply) and (telegram != "n/a"):
						botrep=botrep+"My telegram is "+telegram+". "
					if ("facebook" in reply) and (facebook != "n/a"):
						botrep=botrep+"My facebook is "+facebook+". "
					if (" kik" in reply) and (kik != "n/a"):
						botrep=botrep+"My kik is "+kik+". "
					if ((" phone" in reply) or ("telephone" in reply)) and (kik != "n/a"):
						botrep=botrep+"My phone number is "+phone+". "
					if ("email" in reply) and (email1 != "n/a"):
						botrep=botrep+"My email address is "+email1+". "
					elif ("address" in reply) and (address != "n/a"):
						botrep=botrep+"My home address is "+address+". "
					if ("robot" in reply) or ("bot " in reply):
						botrep="I'm not a robot!"
					if (botrep=="Add me! "):
						replynew=reply.encode('ascii','ignore')
						print "Human: "+replynew
						botrep= cb1.ask(replynew)
						botnew=botrep.lower()
						while ("bot" in botnew) or ("computer" in botnew) or ("human" in botnew) or ("program" in botnew) or ("clever" in botnew) or ("application" in botnew) or ("android" in botnew):
							botrep=cb1.ask(replynew)
							botnew=botrep.lower()
						while ("AI" in botrep):
							botrep=cb1.ask(replynew)
							botnew=botrep.lower()
					else:
						exclamationvar=random.randrange(0,9999)
						botrep=botrep+str(exclamationvar)
					print "Robot: "+botrep
					payload = {'action': 'send_message', 'thread': threadid,'message': botrep}
					r=s.post("http://www.interpals.net/pm.php?thread_id="+threadid, data=payload)
				waitTime = random.randrange(mindelay, maxdelay)
				time.sleep(waitTime)
	run_number += 1
	d.close()
	g.close()
