# Class Library For Map based Web Application Project
import threading
import datetime
import re
from hood.models import Event,Place,User,Event_attenders,Friends,Messages

def Singleton(cls):
	_instances = {}	  # keep classname vs. instance
	def getinstance():
		'''if cls is not in _instances create it
		and store. return the stored instance'''
		if cls not in _instances:
			_instances[cls] = cls()
		return _instances[cls]
	return getinstance
'''
There is only one map object.Thus, it is singleton. Map objects have multiple
regions which are created by users. Some of them is active which means one of the
users is editing the region. The others are passive(static).When a user want to edit
a region, it needs to check intersection with other active regions. Intersected
regions will be deactivated. Deactivation notifies the waiting user to continue.
(See the _inter_condions and activate-deactivate part)
'''
@Singleton
class Map:
	_active_regions = []
	_users_on_map = []
	_inter_conditions = []
	_places = []
	aregionLock = threading.Lock()
	intersectLock = threading.Lock()
	mutexLock = threading.Lock()

	def add_user(self,user):
		self.mutexLock.acquire()
		if user not in User.objects.all()
			u = User(user.name, user.password, user.region, user.x_coord, user.y_coord) #add user to database if doesnt exist
			u.save()
		else:
			print "user is registered already"
		self.mutexLock.release()

	def discard_user(self,user):
		self.mutexLock.acquire()
		if user in User.objects.all():
			user.delete()
		else:
			print "user is not registered"
		self.mutexLock.release()

	def getuser(self,uid):
		result = None
		self.mutexLock.acquire()
		result = User.objects.get(pk=uid):
		self.mutexLock.release()
		return result

	def getusers_on_map(self):
		return User.objects.all()

	def getusers(self,x,y): #dont know what to do bout this
		self.mutexLock.acquire()
		see_users = []
		for user in User.objects.all():
			if user.includes(x,y):
				see_users.append(user)
		self.mutexLock.release()
		return see_users


	# Finds the users that viewing the part of the "region". Those users will be
	# available to see each other in chat and may message each other.Attend each
	# others event and rate them. result of this function will be used to set
	# people_to_chat list of user.
	def usersaround(self,user):
		usersaround = []
		self.mutexLock.acquire()
		for canduser in self._users_on_map:
			r = canduser.getregion()
			if r.intersect(user.getregion()):
				usersaround.append(canduser)
		self.mutexLock.release()
		return usersaround

	def addplace(self,x,y,place):
		place_coord = (place,x,y)
		self._places.append(place_coord)

	def delplace(self,pname,address):
		for place_coord in self._places:
			if pname == place_coord[0].name and address == place_coord[0].location:
				self._places.remove(place_coord)
				break

	def getplacelist(self,region):
		placelist = []
		self.mutexLock.acquire()
		for place_coord in self._places:
			if region.includes(place_coord[1],place_coord[2]):
				placelist.append(place_coord[0])
		self.mutexLock.release()
		return placelist

	def allplaces(self):
		return self._places

	def allevents(self):
		eventlist = []
		for place_c in self._places:
			eventlist = eventlist + place_c[0].getevents()
		return eventlist

	def geteventlist(self,region):
		eventlist = []
		for place_coord in self._places:
			if region.includes(place_coord[1],place_coord[2]):
				eventlist = eventlist + place_coord[0].getevents()
		return eventlist

	def getplace_with_id(self,pid):
		for place_coord in self._places:
			if place_coord[0].pid == pid:
				return place_coord
		return None

	def getplace(self,x,y,margin):
		for place_coord in self._places:
			if	abs(x-place_coord[1])<margin and \
				abs(y-place_coord[2])<margin:
				return place_coord[0]
		return None

	def findplace(self,pname):
		candidates = []
		for place_coord in self._places:
			m = re.search(pname,place_coord[0].name)
			if m:
				candidates.append(place_coord[0])
		return candidates

	def __repr__(self):
		print "yet to implement"

# Before adding event to place Lock related region. No lock inside Event class
class Event:
	def __init__(self,edate,alimit,ename,eid,descript,cap,owner):
		self.eventdate = edate
		self.agelimit = alimit
		self.name = ename
		self.owner = owner
		self.description = descript
		self.capacity = cap
		self._attendants = []
		self.eid = eid
	def attend(self,user):
		self._attendants.append(user)
	
	def leave(self,user):
		self._attendants.remove(user)

	def getattendants(self):
		return self._attendants

	def __str__(self):
		return self.name

	def __repr__(self):
		return str(self.name)

# Before adding place to region Lock whole region. No lock inside Place class
class Place:
	def __init__(self,address,pname,pid):
		self.location = address
		self.name = pname
		self._events = []
		self._ratenum = 0
		self._rate = 0
		self.pid = pid

	def rate(self,value):
		weight = self._ratenum
		self._rate = (self._rate*weight + value)/(weight+1)
		self._ratenum = weight + 1

	def getrate(self):
		return self._rate

	def addevent(self,event):
		if event not in self._events:
			self._events.append(event)
		else:
			print "Duplicate Event"

	def delevent(self,event):
		if event not in self._events:
			print "Cannot find Event"
		else:
			self._events.remove(event)

	def getevents(self):
		return self._events

	def __str__(self):
		return str((self.name,self.pid))

	def __repr__(self):
		return str((self.name,self.pid))
'''
Utilized for group chat and private chat
'''
class Conversation():
	def __init__(self,inituser,map,cid):
		self.inituser = inituser
		self.map = map
		self.cid = cid
		self._users =  []
		self._messages = []
		self._users.append(inituser)
		inituser.addconv(self)
		self.convLock = threading.Lock()

	def getusers(self):
		return self._users

	def getmessages(self):
		return self._messages

	def refresh(self):
		people_allowed = self.map.usersaround(self.inituser)
		for user in self._users:
			if user not in people_allowed:
				self.userleave(user)
				notmessage = NotificationFactory("Leave",user)
				self.addmessage(notmessage)

	def addmessage(self,message):
		self._messages.append(message)

	def userjoin(self,user):
		user.userlock.acquire()
		if user not in self._users:
			self._users.append(user)
			user.addconv(self)
		else:
			print "already in conversation"
		user.userlock.release()

	def userleave(self,user):
		user.userlock.release()
		if user in self._users:
			if user == self.inituser:
				self.inituser = self._users[1]
			self._users.remove(user)
			user.delconv(self)
		else:
			print "not in conversation"
		user.userlock.release()

'''
User has name,password,chatbox,notebox,friendlist,event schedule,privilege
attributes. 
A message may be sent to user. It can be a chat message or a system
notification. Chat messages include info of the user who sends it. Notification
messages includes only the content of message. 
Users add and remove other users as friend. Friend list holds their friends info.
Privilage info will be used for permissions.
'''
class User(object):
	def __init__(self,uname,passw,uid):
		self._messageLock = threading.Lock()
		self.userlock = threading.Lock()
		self._name = uname
		self._password = passw
		self._chat_box = []		# conversation list of the user
		self._friend_requests = []		# pending friend requests
		self._friends = []
		self._schedule = []
		self._not_box = []
		self._region = None
		self._userid = uid

	def __str__(self):
		return str((self._name,self._userid))

	def __repr__(self):
		return str((self._name,self._userid))

	def attachregion(self,region):
		self._region = region

	def detachregion(self):
		self._region = None

	def getregion(self):
		return self._region

	def getuserinfo(self):
		return self._userid, self._name, self._password

	def addconv(self,conversation):
		self._messageLock.acquire()
		if conversation not in self._chat_box:
			self._chat_box.append(conversation)
		else:
			print "conversation is already in chat box"
		self._messageLock.release()

	def delconv(self,conversation):
		self._messageLock.acquire()
		if conversation in self._chat_box:
			self._chat_box.remove(conversation)
		else:
			print "not in chat box"
		self._messageLock.release()

	# users can send message to a conversation that they have involved previously
	def sendmessage(self,message,conversation):
		self._messageLock.acquire()
		if message.val() == "C":
			if conversation in self._chat_box:
				conversation.refresh()
				conversation.addmessage(message)
			else:
				print "not in this conversation"
		elif message.val() == "N":
			self._not_box.append(message)
		else:
			print "message type is NOT allowed"
		self._messageLock.release()
	
	def addfriend(self,person):
		self._friends.append(person)

	def requestfriend(self,person):
		person.sendmessage(NotificationFactory("Friend Request"),None)
		person.addfriendreq(self)

	def addfriendreq(self,person):
		self._friend_requests.append(person)


	def acceptfriendreq(self,person):
		self.addfriend(person)
		person.sendmessage(NotificationFactory("Accept"),None)
		person.addfriend(self)
		self._friend_requests.remove(person)


	def rejectfriendreq(self,person):
		self._friend_requests.remove(person)

	def delfriend(self,person):
		self._friends.remove(person)

	def getchatbox(self):
		return self._chat_box

	def getnotbox(self):
		return self._not_box

	def getschedule(self):
		return self._schedule

	def getfriends(self):
		return self._friends

	def getfriendreqs(self):
		return self._friend_requests

	def addtoschedule(self,event):
		self._schedule.append(event)

	def delfromschedule(self,event):
		self._schedule.remove(event)
'''
Factory design patter for user generation. Admin, place owner, organizer and enduser
'''
def UserFactory(utype,name,passw,uid):
	if utype == "admin":
		return User("admin","adminceng498_2015",-1)
	elif utype == "place owner":
		return User(user.name, user.password, user.region, user.x_coord, user.y_coord)
	elif utype == "organizer":
		return User(name,passw,uid)
	elif utype == "end user":
		return User(name,passw,uid)


'''
Message types and their implementation. There are two types of message which are
Notification and Chat.
'''
class Message(object):
	def val(self):
		return "U"

class Notification(Message):
	def __init__(self,content):
		self.mdate = datetime.time()
		self.mcontent = content

	def val(self):
		return "N"

	def __str__(self):
		return self.mcontent

	def __repr__(self):
		return str(self.mcontent)

class Chat(Message):
	def __init__(self,user,content):
		self.mfrom = user
		self.mdate = datetime.time()
		self.mcontent = content

	def val(self):
		return "C"

	def __str__(self):
		return (self.mfrom,self.mcontent)

	def __repr__(self):
		return str((self.mfrom,self.mcontent))

def NotificationFactory(ntype,user=None):
	if ntype == "Accept":
		return Notification("Friend request accepted")
	elif ntype == "EventAdd":
		return Notification("Event added succesfully")
	elif ntype == "PlaceAdd":
		return Notification("Place added succesfully")
	elif ntype == "Friend Request":
		return Notification("Friend request received")
	elif ntype == "Leave":
		prompt = user.getuserinfo()[0] + "left conversation"
		return Notification(prompt)

class Marker:
	def __init__(self,x,y):
		self.x = x
		self.y = y

'''
Region has info of user who created the region. Basically this eill be created
when user views a portion of map. Every created region will be registered to map
object. When making a change on region, regions will be activated(locked). After
change they will be deactivated(unlocked).That protects everything (place,event etc.)
on the region during change.
'''
class Region:
	def __init__(self,xi,xa,yi,ya):
		self.minx = xi
		self.maxx = xa
		self.miny = yi
		self.maxy = ya
	
	def intersect(self,region):
		if ((region.minx >= self.minx and region.minx <= self.maxx) or (region.maxx <= self.maxx and region.maxx >= self.minx)) \
			and ((region.miny >= self.miny and region.miny <= self.maxy) or (region.maxy <= self.maxy and region.maxy >= self.miny)):
				return True
		else:
				return False

	def includes(self,x,y):
		if (x >= self.minx and x <= self.maxx) and (y >= self.miny and y <= self.maxy):
			return True
		else:
			return False

	def __str__(self):
		return (self.minx,self.miny),(self.maxx,self.maxy)