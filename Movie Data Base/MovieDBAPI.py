import requests
import csv
import os
import time
from apikey import api_key

lang = {'language': 'en-US'}
base_url = 'https://api.themoviedb.org/3/movie/'

#gets the movie associated with the movie ID and returns a json object
def callmovieapi(base_url, movie_number):
	url = base_url + str(movie_number)
	r = requests.get(url, params=api_key)
	if r.status_code == 200:
		raw_movie = r.json()
		return raw_movie
	
#returns a json object of the latest movie ID in the MovieDB database
def latestmovie(base_url):
	url = base_url + 'latest'
	try:
		r = requests.get(url, params=api_key)
		raw_movie = r.json()
	except r.exceptions.HTTPError as err:
		print err
	raw_movie = r.json()
	return raw_movie
	
#prints the header info to the csv file
def printcsvheader(csv_file, column_names):
	try:
		with open(csv_file, 'wb') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = column_names)
			writer.writeheader()
	except IOError as (errno, strerror):
		print("I/O Error({0}): {1}".format(errno, strerror))
	return
	
#prints the list of formated data to the csv file
def printtocsv(csv_file, column_names, movie):
	try:
		with open(csv_file, 'ab') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = column_names)
			for data in movie:
				writer.writerow(data)
	except IOError as (errno, strerror):
		print("I/O Error({0}): {1}".format(errno, strerror))
	return
			

#strips all relevant info from the json object, and creates a list
#also formats in utf-8 since foreign characters are used in MovieDB
def formatmoviedict(raw_movie):
	movie = [{'id': raw_movie['id'],
	          'original_title': raw_movie['original_title'].encode('utf-8'),
	          'overview': raw_movie['overview'].encode('utf-8')}]
	return movie

#validates the data coming from MovieDB
def validate(raw_movie):
    #All the things we think are true about a raw_movie dict
	if raw_movie is None:
		return False
	elif raw_movie['overview'] is None:
		return False
	else:
		return True

# Gets the path for the CSV file
currentPath = os.getcwd()
csv_file = currentPath + "/csv/movies.csv"

#column names used in the csv file
column_names = ['id','original_title','overview'] 


# Exports the header info to a csv file
printcsvheader(csv_file, column_names)

#this is used to avoid hitting the MovieDB API too often
delay_counter = 0

#finds the last entry in MovieDB
total_movies = latestmovie(base_url)

#loops through all movies IDs in MovieDB and extracts the wanted data
for movie_number in range(1,total_movies['id']):

	if delay_counter == delay_counter + 40:
		time.sleep(10)
		delay_counter += 40

	# Gets the data from moviedb api
	raw_movie = callmovieapi(base_url, movie_number)
	if not validate(raw_movie):
		continue
	movie = formatmoviedict(raw_movie)
	printtocsv(csv_file, column_names, movie)
	

	

	
	


