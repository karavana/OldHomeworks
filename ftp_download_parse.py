import threading
import time
import ftplib
import os
import xml.etree.ElementTree
import shutil
import requests
import logging

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
				logging.warning( "Couldn't change to "+self.localdir+" directory, permission prob or directory doesn't exist")
			try:
				
				files = con.nlst()
				lock.acquire()
				for file in files:
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
				logging.info(str(e))				
				raise
	
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
					#try:
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
					except requests.exceptions.RequestException as e:    # This is the correct syntax
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
				

def main():
	logging.basicConfig(filename='potato.log',level=logging.DEBUG)
	logging.info("Started")
	Indir_baba("/home/FTPLocal","/home/FTPFinished","/home/FTPError","127.0.0.1","oguz","oooooooo").start()
	Parse_et_baba("/home/FTPLocal","/home/FTPFinished","/home/FTPError","http://httpbin.org/post").start()		

if __name__ == '__main__':	
	
	main()
				
