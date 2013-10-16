#!/usr/bin/python
import psycopg2
import sys
#import pprint
def addall(tablename):
	global conn
	global cursor	
	baselink = "/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/"
	file = open(baselink + "dock6" + tablename + ".csv", 'r')
	# execute our Query
	#cursor.execute("SELECT * FROM initialcompounds")
	for line in file.readlines():
		#continue
		newint = int(line.split("\t",1)[0])
		restofline = line.split("\t",1)[1]
		tempfile = open("/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/temp.csv", 'w')
		tempfile.write(line)
		tempfile.close()
		for i in range(1): #used to be 8 tries
			try:
				#print "trying %s" % i
				cursor.execute("COPY " + tablename + " FROM '/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/temp.csv' DELIMITER E'\t' CSV;") 
			except Exception as error:
				print("Didn't work:", error)
				newint += 1
				tempfile = open("/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/temp.csv", 'w')
				tempfile.write(str(newint) + "\t" + restofline)
				tempfile.close()
				#print(str(newint) + "\t" + restofline)
				conn.rollback()
			else:
				conn.commit()
				#print "%s breaking" % i
				break	
				
	#cursor.execute("SELECT * FROM initialcompounds")
	# retrieve the records from the database
	#records = cursor.fetchall()
 
	# print out the records using pretty print
	#for r in records:
	#	print(r)
	
def main():
	inputs = []
	initialcompounds = "initialcompounds"
	jobs = "level1_jobs"
	dock6scores = "level1_dock6scores"
	#inputs.append(initialcompounds)
	inputs.append(jobs)
	#inputs.append(dock6scores)
	#jobs = open("/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/dock6jobs.csv", 'r')
	#dock6scores = open("/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/dock6scores.csv", 'r')
	#tempfile = open("/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/temp.csv", 'w')
	conn_string = "host='localhost' dbname='lddb_odorant_tbw' user='kwong23'"
	# print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)
	global conn 
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
 	global cursor
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()

	for table in inputs:
		addall(table)
	#cursor.execute("COPY level1_dock6scores FROM '/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/dock6scores.csv' DELIMITER E'\t' CSV;") 
	#cursor.execute("SELECT * FROM level1_dock6scores")	
	#records = cursor.fetchall()
 	#for r in records:
		#print(r)

	#cursor.execute("COPY level1_jobs FROM '/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/dock6jobs.csv' DELIMITER E'\t' CSV;") 
	#cursor.execute("SELECT * FROM level1_jobs")	
	#records = cursor.fetchall()
 	#for r in records:
		#print(r)
	conn.commit()
	
if __name__ == "__main__":
	main()
