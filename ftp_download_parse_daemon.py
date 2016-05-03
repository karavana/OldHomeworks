#!/usr/bin/env python
import threading
import time
import ftplib
import os
import xml.etree.ElementTree
import shutil
import requests
import logging
import sys
from daemon import Daemon

lock = threading.Condition()

class Indir_baba(threading.Thread):
	def __init__(self,localdir,parsedir,errordir,host,uname,passw):
		threading.Thread.__init__(self)
		self.localdir = localdir
		self.parsedir = parsedir
		self.errordir = errordir
		self.host = host
		self.uname = uname
		self.password = passw

	def run(self):
		while True:
			try:
				con = ftplib.FTP(self.host)
				con.sendcmd("USER "+self.uname)
				con.sendcmd("PASS "+self.password)
			except ftplib.all_errors, e:
				logging.debug(str(e))
			#con.retrlines('LIST')
			try:
				os.chdir(self.localdir)
			except:
				if not os.path.exists(self.localdir):
					logging.info("Specified path "+self.localdir+ "couldn't be found, creating..")
					lock.acquire()
					try:
						os.makedirs(self.localdir)
						os.chmod(self.localdir,0755)
					except:
						logging.info("Directory couldn't be created")
					lock.notifyAll()
					lock.release()
				else:
					logging.info(str(e))
						
			try:
				
				files = con.nlst()
				for file in files:
					lock.acquire()
					if file not in os.listdir(self.parsedir) and file not in os.listdir(self.localdir) and file not in os.listdir(self.errordir):
						con.retrbinary('RETR '+file, open(file,"wb").write)
						logging.info(file + " is downloaded")
					lock.notifyAll()
					lock.release()
				con.quit()
				time.sleep(3) #in order not to send connection request 10k times in a second lol
			except ftplib.error_perm, resp:
				if str(resp) == "550 No files found":
					logging.warning("No files in this directory")
				else:
					logging.debug(str(resp))
				lock.notifyAll()
				lock.release()
				con.quit()
			except ftplib.all_errors, e:
				logging.debug(str(e))
				lock.notifyAll()
				lock.release()
				con.quit()
			except Exception, e:
				if not os.path.exists(self.errordir):
					logging.info("Directory "+self.errordir+"doesn't exist, creating.." )
					lock.acquire()
					try:
						os.makedirs(self.errordir)
						os.chmod(self.errordir,0755)
					except:
						logging.info("Directory couldn't be created")
					lock.notifyAll()
					lock.release()
				else:
					logging.info(str(e))				
				
	
class Parse_et_baba(threading.Thread):
	def __init__(self,localdir,parsedir,errordir,posthost):
		threading.Thread.__init__(self)
		self.localdir = localdir
		self.parsedir = parsedir
		self.errordir = errordir
		self.posthost = posthost
		
	def run(self):
		while True:
			is_error = False
			if os.listdir(self.localdir):
				
				for file in os.listdir(self.localdir):
					lock.acquire()
					try:
						xml_file = xml.etree.ElementTree.parse(self.localdir+"/"+file).getroot()
						logging.info(file +" is parsed")
						lock.notifyAll()
						lock.release()
					except xml.etree.ElementTree.ParseError as err:
						is_error = True
						logging.debug(err.msg)
						lock.notifyAll()
						lock.release()
					#try: #change this to get xml attributes
						#sitename = xml_file.attrib["Sitename"]
						#devicename = xml_file.attrib["Devicename"]
						#divisionId = xml_file.attrib["DivisionId"]
						#siteId = xml_file.attrib["SiteId"]
						#deviceId = xml_file.attrib["DeviceId"]
						#for info in xml_file.iter("Count"):
							#info.attrib #this will give count info as a dict object
					#except:
						#print "Couldn't get information from xml, specified key or attribute not found"
					try:
						r = requests.post(self.posthost,data = {'key':'value'})
					except requests.exceptions.RequestException as e:    
						logging.debug(e)

					try:
						lock.acquire()
						if is_error:
							print self.localdir
							print self.errordir
							print file
							shutil.move(self.localdir+"/"+file, self.errordir+"/"+file)
							is_error = False
						else:
							shutil.move(self.localdir+"/"+file, self.parsedir+"/"+file)
						lock.notifyAll()
						lock.release()
					except shutil.Error, exc:
						logging.debug(str(exc))
						lock.notifyAll()
						lock.release()
			
class Ariza(Daemon):
	def run(self): #override Daemon's run method
		os.chdir("/var/log")
		logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='potato.log',level=logging.DEBUG)
		logging.info("Started")
		Indir_baba("/home/FTPLocal","/home/FTPFinished","/home/FTPError","127.0.0.1","oguz","oooooooo").start()
		Parse_et_baba("/home/FTPLocal","/home/FTPFinished","/home/FTPError","http://httpbin.org/post").start()		




if __name__ == '__main__':	
	
	daemon = Ariza('/var/run/potato.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
				
