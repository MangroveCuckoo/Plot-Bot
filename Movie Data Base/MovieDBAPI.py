import requests
import csv
import os
import time
from apikey import api_key

lang = {'language': 'en-US'}
base_url = 'https://api.themoviedb.org/3/movie/'

def callmovieapi(base_url, movie_number):
	url = base_url + str(movie_number)
	r = requests.get(url, params=api_key)
	if r.status_code == 200:
		raw_movie = r.json()
		return raw_movie
	
def latestmovie(base_url):
	url = base_url + 'latest'
	try:
		r = requests.get(url, params=api_key)
		raw_movie = r.json()
	except r.exceptions.HTTPError as err:
		print err
	raw_movie = r.json()
	return raw_movie
	
def printcsvheader(csv_file, column_names):
	try:
		with open(csv_file, 'wb') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = column_names)
			writer.writeheader()
	except IOError as (errno, strerror):
		print("I/O Error({0}): {1}".format(errno, strerror))
	return
	
def printtocsv(csv_file, column_names, movie):
	try:
		with open(csv_file, 'ab') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = column_names)
			for data in movie:
				writer.writerow(data)
	except IOError as (errno, strerror):
		print("I/O Error({0}): {1}".format(errno, strerror))
	return
			

def formatmoviedict(raw_movie):
	movie = [{'id': raw_movie['id'],
	          'original_title': raw_movie['original_title'].encode('utf-8'),
	          'overview': raw_movie['overview'].encode('utf-8')}]
	return movie


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

column_names = ['id','original_title','overview'] 


# Exports the header info to a csv file
printcsvheader(csv_file, column_names)


delay_counter = 0
total_movies = latestmovie(base_url)

#this loop will eventually end in the id number of total_movies
#for movie_number in range(1,total_movies['id']):
for movie_number in range(550,550):

	if delay_counter == delay_counter + 40:
		time.sleep(10)
		delay_counter += 40

	# Gets the data from moviedb api
	raw_movie = callmovieapi(base_url, movie_number)
	if not validate(raw_movie):
		continue
	movie = formatmoviedict(raw_movie)
	printtocsv(csv_file, column_names, movie)
	

	

	
	


