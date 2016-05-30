import time
from datetime import date
from pymongo import MongoClient

def get_db():
    
    client = MongoClient('localhost:27017')
    db = client.myFirstMB
    return db

def add_country(db):
    db.countries.insert({"created_on" : time.time(),"name" : "Canada"})
    
def get_country(db):
    return db.countries.find_one()

if __name__ == "__main__":

	db = get_db() 
	a = time.time()
	for i in range(1000000):
		add_country(db)
		if(i%50000 == 0):
			print i
	b = time.time()
	c = (str)(b-a)
	print "it took "+c+"secs to complete"
    
