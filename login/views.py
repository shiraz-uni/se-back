from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import secrets
from .models import StudentN, cred, SelfListN, TransactionN, FoodMenuN, CouponN
from datetime import datetime
from datetime import timedelta


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
            cred(username=user, ti=time.time(), token=tok).save()
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
            st = cred.objects.get(token=token)
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
            st = cred.objects.get(token=token)
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
            st = cred.objects.get(token=token)
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

            te = TransactionN.objects.get(student=temp_user_id)
            # for _ in te:
            #	transactions_dict[str(_.date)] = {_.bank : str(_.price)}
            transactions_dict[str(te.date)] = {te.bank: str(te.price)}
            data["transactions"] = transactions_dict

            coupons_dict = {}

            cq = CouponN.objects.get(student=temp_user_id)
            # for _ in cq:
            #	coupons_dict["is_active"] = str(_.state)
            #	coupons_dict["food"] = FoodMenuN.objects.get(Key_id = _.food).food_name1
            #	coupons_dict["self"] = SelfListN.objects.get(self_id = _.self_id).self_name

            coupons_dict["is_active"] = str(cq.state)
            # coupons_dict["self"] = SelfListN.objects.get(self_id = cq.self_id).self_name

            data["coupons"] = coupons_dict

            return JsonResponse(data)
        else:
            return HttpResponse('You are not lgged in')
    else:
        return HttpResponse('invalid request')


def get_saterday(today):
    if today.weekday() < 5:
        saturday = datetime(today.year, today.month, today.day - today.weekday() - 2)
    elif today.weekday() > 5:
        saturday = datetime(today.year, today.month, today.day - 1)
    else:
        saturday = today
    return saturday


def get_week_data(data, day):
    saterday = get_saterday(day)
    sf_data = {}
    for _ in range(7):
        sf_data["price1"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_),
                                                           meal_type="breakfast").price1
        sf_data["price2"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_),
                                                           meal_type="breakfast").price2
        sf_data["food_name1"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_),
                                                               meal_type="breakfast").food_name1
        sf_data["food_name2"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_),
                                                               meal_type="breakfast").food_name1
        sf_data["key_id"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_),
                                                           meal_type="breakfast").credit
        data["date", "meal_type"] = sf_data
    for _ in range(7):
        sf_data["price1"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_), meal_type="dinner").price1
        sf_data["price2"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_), meal_type="dinner").price2
        sf_data["food_name1"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_),
                                                               meal_type="dinner").food_name1
        sf_data["food_name2"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_),
                                                               meal_type="dinner").food_name1
        sf_data["key_id"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_), meal_type="dinner").credit
        data["date", "meal_type"] = sf_data
    for _ in range(7):
        sf_data["price1"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_), meal_type="lunch").price1
        sf_data["price2"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_), meal_type="lunch").price2
        sf_data["food_name1"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_),
                                                               meal_type="lunch").food_name1
        sf_data["food_name2"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_),
                                                               meal_type="lunch").food_name1
        sf_data["key_id"] = FoodMenuN.objects.all().filter(data=saterday + timedelta(days=_), meal_type="lunch").credit
        data["date", "meal_type"] = sf_data


def get_week_coupons(data, day, std):
    saterday = get_saterday(day)
    coupon = {}
    lst = list(CouponN.objects.filter(student=std).filter(food__date__gte=saterday,
                                                          food__date__lte=saterday + timedelta(days=6)))
    i = 0
    while i < len(lst):
        coupon["state"] = lst[i].state
        coupon["coupon_id"] = lst[i].coupon_id
        coupon["food"] = lst[i].food
        coupon["self_id"] = lst[i].self_id
        data["food"] = coupon


@csrf_exempt
def self_data(request):
    '''remove the token and the username for the database'''
    if request.method == 'GET':
        return HttpResponse('Post')
    elif request.method == 'POST':
        req = request.read()
        j = json.loads(req)
        token = j['token']
        if token_check(token):
            st = cred.objects.get(token=token)
            temp_user_id = st.username
            data = {}
            get_week_data(data, datetime.now())
            get_week_coupons(data, datetime.now(), st)

            return JsonResponse(data)
        else:
            return HttpResponse('You are not lgged in')
    else:
        return HttpResponse('invalid request')


