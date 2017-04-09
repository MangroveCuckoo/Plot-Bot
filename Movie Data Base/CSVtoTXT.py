import csv
import sys
import os

#text path
currentPath = os.getcwd()
txt_file = currentPath + "/text/movies.txt"

# csv path
currentPath = os.getcwd()
csv_file = currentPath + "/csv/movies.csv"

#names of the columns in the movies.csv file
column_names = ['id','original_title','overview'] 

#open txt file
textfile = open(txt_file, 'w')

#open csv file
try:
	with open(csv_file, 'rb') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames = column_names)
		for row in reader:
			textfile.write(row['original_title'] + '|||' + row['overview'] +'\n')
		#print out title & summary (rows 2 & 3) into txt file
		#print them out as pairs, with ||| separating each title & summary
	
except IOError as (errno, strerror):
	print("I/O Error({0}): {1}".format(errno, strerror))
	
textfile.close()


#iterate over rows
#example: for row in 'filename'


#close txt file
#close csv file


