
import hoodlib as hood
import socket
import re
import sys
import datetime
from threading import Thread,Lock,Condition

class UserInteractionAgent(Thread):
    def __init__(self,conn,addr,map,users):
        self.users = users
        self.map = map
        self.conn = conn
        self.claddr = addr
        Thread.__init__(self)
    def run(self):
        global conversation_id_count
        data = self.conn.recv(1024)
        if re.search('[ 	]+',data):
            command = data.split(' ')[0]
            arg = data.split(' ')[1:]
        else:
            command,arg = data,''

        if command == "usersaround": #args: uid
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0] and user in self.map.getusers_on_map():
                    print self.map.usersaround(user)
                    user.userlock.release()
                    break
                user.userlock.release()
            print "COULD NOT FIND USER"

        elif command == "friendreq": #args: uid index
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0] and user in self.map.getusers_on_map():
                    aroundlist = self.map.usersaround(user)
                    try:
                        person = aroundlist[int(arg[1])]
                    except:
                        print "PERSON FETCH ERROR"
                        return
                    user.addfriendreq(person)
                    user.userlock.release()
                    break
                user.userlock.release()
            print "COULD NOT FIND USER"

        elif command == "acceptfriendreq": #args: uid index
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0]:
                    reqlist = user.getfriendreqs()
                    try:
                        person = reqlist[int(arg[1])]
                    except:
                        print "PERSON FETCH ERROR"
                        return
                    user.acceptfriendreq(person)
                    user.userlock.release()
                    break
                user.userlock.release()
            print "COULD NOT FIND USER"

        elif command == "rejectfriendreq": #args: uid index
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0]:
                    reqlist = user.getfriendreqs()
                    try:
                        person = reqlist[int(arg[1])]
                    except:
                        print "PERSON FETCH ERROR"
                        return
                    user.rejectfriendreq(person)
                    user.userlock.release()
                    break
                user.userlock.release()
            print "COULD NOT FIND USER"

        elif command == "delfriend": #args: uid index
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0]:
                    flist = user.getfriends()
                    try:
                        person = flist[int(arg[1])]
                    except:
                        print "PERSON FETCH ERROR"
                        return
                    user.delfriend(person)
                    user.userlock.release()
                    break
                user.userlock.release()
            print "COULD NOT FIND USER"

        elif command == "startconv": #args: uid index
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0] and user in self.map.getusers_on_map():
                    aroundlist = self.map.usersaround(user)
                    try:
                        person = aroundlist[int(arg[1])]
                    except:
                        print "PERSON FETCH ERROR"
                        return
                    conv = hood.Conversation(user,map,conversation_id_count)
                    conversation_id_count += 1
                    conv.userjoin(person)
                    user.userlock.release()
                    break
                user.userlock.release()
            print "COULD NOT FIND USER"

        elif command == "addtoconv": #args: uid index_conv imdex_person
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0]:
                    convlist = user.getchatbox()
                    try:
                        conv = convlist[int(arg[1])]
                    except:
                        print "CONVERSATION FETCH ERROR"
                        return
                    if conv.inituser != user:
                        print "NOT ALLOWED TO ADD PEOPLE"
                        return
                    personlist = self.map.usersaround(user)
                    try:
                        person = personlist[int(arg[2])]
                    except:
                        print "CONVERSATION FETCH ERROR"
                        return
                    conv.userjoin(person)
                    user.userlock.release()
                    break
                user.userlock.release()
            print "COULD NOT FIND USER"

        elif command == "sendmessage": #args: uid index_of_conv message
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0]:
                    chatlist = user.getchatbox()
                    try:
                        conv = chatlist[int(arg[1])]
                    except:
                        print "CONV FETCH ERROR"
                        return
                    user.sendmessage(arg[2],conv)
                    user.userlock.release()
                    break
                user.userlock.release()
            print "COULD NOT FIND USER"

class MapModifierAgent(Thread):
    def __init__(self,conn,addr,map,users):
        self.mutex = Lock()
        self.users   = users
        self.map     = map
        self.conn = conn
        self.claddr = addr
        Thread.__init__(self)
    def run(self):
        global user_id_count
        global place_id_count
        global event_id_count
        data = self.conn.recv(1024)
        if re.search('[ 	]+',data):
            command = data.split(' ')[0]
            arg = data.split(' ')[1:]
        else:
            command,arg = data,''

        if command == "addplace":   # args: x,y "address" "placename" "uid"
            coordlst = arg[0].split(",")             # (x,y)
            myplace = hood.Place(arg[1],arg[2],place_id_count)     # adress , name
            place_id_count += 1
            for user in self.map.getusers_on_map():
                user.userlock.acquire()
                if int(arg[3]) == user.getuserinfo()[0]:
                    self.map.activate(user.getregion())
                    self.map.addplace(float(coordlst[0]),float(coordlst[1]),myplace)
                    self.map.deactivate(user.getregion())
                    user.userlock.release()
                    break
                user.userlock.release()
            print "COULD NOT FIND USER"

        elif command == "getplaces": # args uid
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0]:
		   if user.getregion() is not None:
		            self.map.activate(user.getregion())
		            print user
		            if len(self.map.getplacelist(user.getregion())) >= 1:
				res = ""				
				for tupleo in self.map.getplacelist(user.getregion()):
					res += tupleo.name
					res += " "
			    	self.conn.send(res)
		            else:
				self.conn.send(" ")
			    self.map.deactivate(user.getregion())
		            user.userlock.release()
		            break
		   else:
		    	    self.conn.send(" ")
                user.userlock.release()
            print "COULD NOT FIND USER"

        elif command == "getevents": # args uid
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0] and user in self.map.getusers_on_map():
                    self.map.activate(user.getregion())
                    print self.map.geteventlist(user.getregion())
                    self.map.deactivate(user.getregion())
                    user.userlock.release()
                    break
                user.userlock.release()
            print "COULD NOT FIND USER"

        elif command == "delplace": # args: pass uid index
            if arg[0] == "adminceng498_2015":
                for user in self.users:
                    user.userlock.acquire()
                    if int(arg[1]) == user.getuserinfo()[0]:
                        self.map.activate(user.getregion())
                        placelist = self.map.getplacelist(user.getregion())
                        try:
                            place = placelist[int(arg[2])]
                        except:
                            print "PLACE FETCH ERROR"
                            return
                        self.map.delplace(place.name,place.location)
                        print "deleted",place.name,place.location
                        self.map.deactivate(user.getregion())
                        user.userlock.release()
                        break
                    user.userlock.release()
                print "COULD NOT FIND USER"
            else:
                print "wrong password"

        elif command == "addevent":     # args: "ename" "descp" "agelimit" capacity index [eventowner]
            ename = arg[0]
            descp = arg[1]
            age   = int(arg[2])
            cap   = int(arg[3])
            pindex = int(arg[4])
            user = self.map.getuser(int(arg[5]))
            if user is None:
                print "USER FETCH ERROR"
                return
            user.userlock.acquire()
            self.map.activate(user.getregion())
            placelist = self.map.getplacelist(user.getregion())
            try:
                place = placelist[pindex]
            except:
                print "PLACE FETCH ERROR"
                return
            event = hood.Event(datetime.time(),age,ename,event_id_count,descp,cap,user)
            event_id_count += 1
            place.addevent(event)
            self.map.deactivate(user.getregion())
            user.userlock.release()

        elif command == "getschedule":    # args: uid
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0]:
                    schedule = user.getschedule()
                    print schedule
                    user.userlock.release()
                    break
                user.userlock.release()
            print "COULD NOT FIND USER"

        elif command == "getrate":  # args uid index
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0]:
                    self.map.activate(user.getregion())
                    placelist = self.map.getplacelist(user.getregion())
                    place = placelist[int(arg[1])]
                    print place.getrate()
                    self.map.deactivate(user.getregion())
                    user.userlock.release()
                    break
                user.userlock.release()

        elif command == "rate":    # args: uid index value
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0]:
                    self.map.activate(user.getregion())
                    placelist = self.map.getplacelist(user.getregion())
                    place = placelist[int(arg[1])]
                    place.rate(float(arg[2]))
                    self.map.deactivate(user.getregion())
                    user.userlock.release()
                    break
                user.userlock.release()

        elif command == "attend": # args: uid index
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0]:
                    self.map.activate(user.getregion())
                    eventlist = self.map.geteventlist(user.getregion())
                    event = eventlist[int(arg[1])]
                    event.attend(user)
                    user.addtoschedule(event)
                    self.map.deactivate(user.getregion())
                    user.userlock.release()
                    break
                user.userlock.release()

        elif command == "leave": # args: uid index_schedule
            for user in self.users:
                user.userlock.acquire()
                if int(arg[0]) == user.getuserinfo()[0]:
                    self.map.activate(user.getregion())
                    eventlist = user.getschedule()
                    event = eventlist[int(arg[1])]
                    event.leave(user)
                    user.delfromschedule(event)
                    self.map.deactivate(user.getregion())
                    user.userlock.release()
                    break
                user.userlock.release()

        elif command == "changeregion": # args: xm,ym xn,yn uid
            mintuple = arg[0].split(",")
            maxtuple = arg[1].split(",")
            r = hood.Region(float(mintuple[0]),float(maxtuple[0]),float(mintuple[1]),float(maxtuple[1]))
            self.mutex.acquire()
            for user in self.users:
                user.userlock.acquire()
                if int(arg[2]) == user.getuserinfo()[0]:
                    self.map.activate(r)
                    if user not in self.map.getusers_on_map():
                        user.attachregion(r)
                        self.map.add_user(user)
                    else:
                        self.map.discard_user(user)
                        user.attachregion(r)
                        self.map.add_user(user)
                    self.map.deactivate(r)
                    user.userlock.release()
                    break
                user.userlock.release()
            self.mutex.release()

        elif command == "createuser":   # args: "utype" "uname" "pass" ["uid"]
            self.mutex.acquire()
            user = hood.UserFactory(arg[0],arg[1],arg[2],user_id_count)
            user.addr = addr
            self.users.append(user)
            user_id_count += 1
            print "created",user,user_id_count
            self.mutex.release()

        elif command == "deluser":      # args: uid
            self.mutex.acquire()
            for user in self.users:
                user.userlock.acquire()
                if user.getuserinfo()[0] == int(arg[0]):
                    if user in self.map.getusers_on_map():
                        self.map.activate(user.getregion())
                        self.map.discard_user(user)
                        self.map.deactivate(user.getregion())
                    self.users.remove(user)
                    user.userlock.release()
                    break
                user.userlock.release()
            self.mutex.release()

        elif command == "show":
	    print addr
            print self.users
	    self.conn.send(str(users))
            print self.map.getusers_on_map()
	    self.conn.send(str(self.map.getusers_on_map()))
            names = []
            for place in self.map.allplaces():
                names.append(place[0].name)
            print names
	    self.conn.send(str(names))
            names = []
            for event in self.map.allevents():
                names.append(event.name)
            print names
	    self.conn.send(str(names))
map = hood.Map()
users = []
user_id_count = 0
place_id_count = 0
event_id_count = 0
conversation_id_count = 0

HOST = 'localhost'
PORT = 5001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

while True:
    conn, addr = s.accept()

    print 'Connected by', addr
    a = MapModifierAgent(conn,addr,map,users)
    b = UserInteractionAgent(conn,addr,map,users)
    a.start()
    b.start()
