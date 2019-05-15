#from django.shortcuts import render
# TODO solve credentials check

from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import sqlite3
import secrets
from ..database.models import Student


def cridentials_test(user, password):
	#'''check credentials against the hardcoded database'''
	# if user == 'admin' and password == 'admin':
	#	return True
	c = Student.objects.get(studentNo=user, password=password)
	if c.password == password:
		return True


def token_check(token):
	connection = sqlite3.connect('ucon.db')
	cursor = connection.cursor()
	cursor.execute("select * from cred;")
	cc = cursor.fetchone()
	while cc is not None:
		if cc[2] == token:
			connection.close()
			return True
	connection.close()
	return False

@csrf_exempt
def login(request):

	''' the user and password is preferably hashed and in a json object sent.
	if the username and password are valid I generate a token and send it
	to the device and store it aswell. Throughout the usage in evey request the
	client must imclude the token in a json in the request to be validated
	againts the valid tokens and if not wither it has been signed out automatically
	or any other error. A timer will start and just let the person use this for 30' if or the person calls
	the logout and after checking the toke the user is removed fro the local
	database of logged in people. DO NOT FORGET TO BLOCK GET REQUESTS.'''
	if request.method == 'GET':
		return HttpResponse('Post')
	elif request.method == 'POST':
		req = request.read()
		j = json.loads(req)
		user = j['user']
		password = j['password']
		if cridentials_test(user, password):
			connection = sqlite3.connect('ucon.db')
			cursor = connection.cursor()
			tok = secrets.token_hex(16)
			cursor.execute("insert into cred values ('" + user + "', " + str(time.time()) + ", '" + str(tok) + "');")
			connection.commit()
			connection.close()
			return HttpResponse(tok)
		else:
			return HttpResponse("Wrong credentials")
	else:
		return HttpResponse('invalid request')

		'''computer_science_notes safari$ curl -d '{"user" : "admin", "password":"admin"}' -H "Contenon/json" -X POST localhost:8080/login/login'''

@csrf_exempt
def already_in(request):
	'''
	if the persone comes out of the software client side and wants to know if still logged in
	'''
	if request.method == 'GET':
		return HttpResponse('Post')
	elif request.method == 'POST':
		req = request.read()
		j = json.loads(req)
		token = j['token']
		if token_check(token):
			connection = sqlite3.connect('ucon.db')
			cursor = connection.cursor()
			cursor.execute("select * from cred;")
			cc = cursor.fetchone()
			while cc is not None:
				if cc[2] == str(token):
					connection.close()
					return HttpResponse(token)
				cc.fetchone()
			connection.close()
			return HttpResponse('You are not lgged in')
		else:
			return HttpResponse("Wrong credentials")
	else:
		return HttpResponse('invalid request')
		'''curl -d '{"token" : "16998f6a2d1c3eadf8bff1a40c439d68"}' -H "Content-Type: ap applidation/json" -X POST localhost:8080/login/login'''
		'''computer_science_notes safari$ curl -d '{"user" : "admin", "password":"admin"}' -H "Contenon/json" -X POST localhost:8080/login/already_in'''

@csrf_exempt
def logout(request):
	'''remove the token and the username for the database'''
	if request.method == 'GET':
		return HttpResponse('Post')
	elif request.method == 'POST':
		req = request.read()
		j = json.loads(req)
		token = j['token']
		if token_check(token):
			connection = sqlite3.connect('ucon.db')
			cursor = connection.cursor()
			cursor1 = connection.cursor()
			cursor.execute("select * from cred;")
			cc = cursor.fetchone()
			while cc is not None:
				if cc[2] == str(token):
					cursor1.execute("delete from cred where token = '" + token +"';")
					connection.commit()
					connection.close()
					return HttpResponse('logged out')
				cc.fetchone()
			return HttpResponse('You are not lgged in')
		else:
			return HttpResponse("Wrong credentials")
	else:
		return HttpResponse('invalid request')

def test(request):
	return JsonResponse({'token': 'some123random123token'})
