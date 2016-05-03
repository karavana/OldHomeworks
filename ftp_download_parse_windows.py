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
				con.sendcmd("USER "+ self.uname)
				con.sendcmd("PASS" + self.password)
			except ftplib.all_errors, e:
				logging.debug(str(e))
			try:
				os.chdir(self.localdir)
			except Exception, e:
				logging.warning( "Couldn't change to local download directory")
				if not os.path.exists(self.localdir):
					logging.info("Specified path "+self.localdir+" couldn't be found, creating....")
					lock.acquire()
					try:
						os.makedirs(self.localdir)
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
				time.sleep(3)
			except ftplib.all_errors, e:
				logging.debug(str(e))
				lock.notifyAll()
				lock.release()
				con.quit()
				time.sleep(3)
			except Exception, e:
				logging.debug(str(e))
				time.sleep(3)
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
			try:
				if os.listdir(self.localdir):
					
					for file in os.listdir(self.localdir):
						try:
							lock.acquire()
							xml_file = xml.etree.ElementTree.parse(self.localdir+"\\"+file).getroot()
							logging.info(file +" is parsed")
							lock.notifyAll()
							lock.release()
							#sitename = xml_file.attrib["Sitename"]
							#devicename = xml_file.attrib["Devicename"]
							#divisionId = xml_file.attrib["DivisionId"]
							#siteId = xml_file.attrib["SiteId"]
							#deviceId = xml_file.attrib["DeviceId"]
							#for info in xml_file.iter("Count"):
								#info.attrib #this will give count info as a dict object
						#except:
							#print "Couldn't get information from xml, specified key or attribute not found"
							r = requests.post(self.posthost,data = {'key':'value'})
						
							lock.acquire()
							if is_error and os.path.exists(self.errordir):
								shutil.move(self.localdir+"\\"+file,self.errordir+"\\"+file)
								is_error = False
							elif os.path.exists(self.errordir):
								shutil.move(self.localdir+"\\"+file,self.parsedir+"\\"+file)
							lock.notifyAll()
							lock.release()
						except xml.etree.ElementTree.ParseError as err:
							is_error = True
							logging.debug(err.msg)
							lock.notifyAll()
							lock.release()
							time.sleep(3)
						except requests.exceptions.RequestException as e:    # This is the correct syntax
							logging.debug(e)
							time.sleep(3)
						except shutil.Error, exc:
							logging.debug(str(exc))
							lock.notifyAll()
							lock.release()
							time.sleep(3)
			except Exception, e:
				if not os.path.exists(self.localdir):
					logging.info("Specified path couldn't be found, creating....")
					lock.acquire()
					try:
						os.makedirs(self.localdir)
					except:
						logging.info("Directory couldn't be created")
					lock.notifyAll()
					lock.release()
				else:
					logging.debug(str(e))
				

def main():
	logging.basicConfig(filename='potato.log',level=logging.DEBUG)
	logging.info("Started")
	Indir_baba("C:\\Users\\PC\\Desktop\\FTPLocal","C:\\Users\\PC\\Desktop\\FTPFinished","C:\\Users\\PC\\Desktop\\FTPError","127.0.0.1","admin","").start()
	Parse_et_baba("C:\\Users\\PC\\Desktop\\FTPLocal","C:\\Users\\PC\\Desktop\\FTPFinished","C:\\Users\\PC\\Desktop\\FTPError","http://httpbin.org/post").start()		

if __name__ == '__main__':	
	
	main()
				
