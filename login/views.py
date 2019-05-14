#from django.shortcuts import render
# TODO solve credentials check

from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import sqlite3
import secrets


def cridentials_test(user, password):
	'''check credentials against the hardcoded database'''
	if user == 'admin' and password == 'admin':
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
	#return HttpResponse(len(request.read()))
	#return JsonResponse({'foo': 'bar'})
	#return HttpResponse(request.META['HTTP_USER_AGENT'])
	#return HttpResponse(request.META['REMOTE_ADDR']) # for getting the ip
	if request.method == 'POST':
		return HttpResponse('' + ' and Your post body is ' + request.read())
	return HttpResponse('' + '''

<head>
<style>
div {
  width: 100px;
  height: 100px;
  background-color: red;
  position: relative;
  -webkit-animation-name: example; /* Safari 4.0 - 8.0 */
  -webkit-animation-duration: 4s; /* Safari 4.0 - 8.0 */
  animation-name: example;
  animation-duration: 1s;
  animation-iteration-count: 10000;
}

/* Safari 4.0 - 8.0 */
@-webkit-keyframes example {
  0%   {background-color:red; left:0px; top:0px;}
  25%  {background-color:yellow; left:200px; top:0px;}
  50%  {background-color:blue; left:200px; top:200px;}
  75%  {background-color:green; left:0px; top:200px;}
  100% {background-color:red; left:0px; top:0px;}
}

/* Standard syntax */
@keyframes example {
  0%   {background-color:red; left:0px; top:0px;}
  25%  {background-color:yellow; left:200px; top:0px;}
  50%  {background-color:blue; left:200px; top:200px;}
  75%  {background-color:green; left:0px; top:200px;}
  100% {background-color:red; left:0px; top:0px;}
}
</style>
</head>
<body>

<div></div>

</body>


		''')


'''curl -d '{"token" : "ef7f07722a8bf1bdac032595ff698c1a"}' -H "Content-Type: applidation/json" -X POST localhost:8080/login/already_in
'''

'''curl -d '{"token" : "ef7f07722a8bf1bdac032595ff698c1a"}' -H "Content-Type: applidation/json" -X POST localhost:8080/login/already_in
'''
