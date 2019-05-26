from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import secrets
from .models import StudentN, cred, SelfListN, TransactionN, FoodMenuN, CouponN


def cridentials_test(user, password):
	c = StudentN.objects.get(student_no=user)
	if c is not None and c.password == password:
		return True


def token_check(token):
	st = cred.objects.get(token=token)
	if st is not None:
		return True
	else:
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
			tok = secrets.token_hex(16)
			cred(username = user, ti = time.time(), token = tok).save()
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
			st = cred.objects.get(token = token)
			if st is not None:
				return HttpResponse(token)
			else:
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
			st = cred.objects.get(token = token)
			if st is not None:
				st.delete()
				return HttpResponse("OK")
			else:
				return HttpResponse('You are not lgged in')
		else:
			return HttpResponse("Wrong credentials")
	else:
		return HttpResponse('invalid request')

def test(request):
	return JsonResponse({'token': 'some123random123token'})

@csrf_exempt
def week_data(request):
	'''remove the token and the username for the database'''
	if request.method == 'GET':
		return HttpResponse('Post')
	elif request.method == 'POST':
		req = request.read()
		j = json.loads(req)
		token = j['token']
		if token_check(token):
			st = cred.objects.get(token = token)
			temp_user_id = st.username
			data = {}
			st_id = {}
			sto = StudentN.objects.get(student_no=temp_user_id)
			st_id["first_name"] = sto.first_name
			st_id["last_name"] = sto.last_name
			st_id["student_no"] = sto.student_no
			st_id["student_type"] = sto.std_type
			st_id["credit"] = sto.credit
			data["student_id"] = st_id
			self_list = {}
			sl = SelfListN.objects.all()
			for _ in sl:
				self_list[_.self_id] = _.self_name

			data["self_list"] = self_list
			transactions_dict = {}

			te = sto.transactionn_set.all()
			#for _ in te:
			#	transactions_dict[str(_.date)] = {str(_.bank) : str(_.price)}
			#transactions_dict[str(te.date)] = {te.bank : str(te.price)}
			#data["transactions"] = transactions_dict

			coupons_dict = {}

			cq = sto.couponn_set.all()
			#for _ in cq:
			#	coupons_dict["is_active"] = str(_.state)
			#	coupons_dict["food"] = FoodMenuN.objects.get(key_id = _.food).food_name1
			#	coupons_dict["self"] = SelfListN.objects.get(self_id = _.self_id).self_name
			#	coupons_dict["is_active"] = str(cq.state)

			data["coupons"] = coupons_dict

			return JsonResponse(data)
		else:
				return HttpResponse('You are not lgged in')
	else:
		return HttpResponse('invalid request')
