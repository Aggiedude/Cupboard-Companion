import urllib2
import json
import string
import base64
import re

def replace_chars(query):
	query = string.replace(query, "'", '%27')
	query = string.replace(query, '"', '%27')
	query = string.replace(query, '+', '%2b')
	query = string.replace(query, ' ', '%20')
	query = string.replace(query, ':', '%3a')
	query = string.replace(query, '(', '%28')
	query = string.replace(query, ')', '%29')
	query = string.replace(query, '[', '%5b')
	query = string.replace(query, ']', '%5d')
	return query

def main():
	#credentials structure: _app_id=app-id&_app_key=app-key
	yummlyAppID = " " #appID goes here
	yummlyAppKey = " " #appKey goes here
	yummlyCredentials = '%s=%s&%s=%s' % ('_app_id', yummlyAppID, '_app_key', yummlyAppKey)
	
	query = "'fish tacos'"
	urlQuery = 'q=' + replace_chars(query)
	
	searchParamenters = urlQuery
	
	url = 'http://api.yummly.com/v1/api/recipes?%s&%s' % (yummlyCredentials, searchParamenters)
	
	print url
	
	request = urllib2.Request(url)
	requestOpener = urllib2.build_opener()
	response = requestOpener.open(request)
	
	results = json.load(response)
	print results
	
if __name__ == '__main__':
	main()