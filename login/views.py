from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import secrets
from .models import StudentN, cred, SelfListN, TransactionN, FoodMenuN, CouponN
from datetime import datetime
from datetime import timedelta
import math


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


# @csrf_exempt
# def week_data(request):
#     '''remove the token and the username for the database'''
#     if request.method == 'GET':
#         return HttpResponse('Post')
#     elif request.method == 'POST':
#         req = request.read()
#         j = json.loads(req)
#         token = j['token']
#         if token_check(token):
#             st = cred.objects.get(token=token)
#             temp_user_id = st.username
#             data = {}
#             st_id = {}
#             sto = StudentN.objects.get(student_no=temp_user_id)
#             st_id["first_name"] = sto.first_name
#             st_id["last_name"] = sto.last_name
#             st_id["student_no"] = sto.student_no
#             st_id["student_type"] = sto.std_type
#             st_id["credit"] = sto.credit
#             data["student_id"] = st_id
#             self_list = {}
#             sl = SelfListN.objects.all()
#             for _ in sl:
#                 self_list[_.self_id] = _.self_name
#
#             # data["self_list"] = self_list
#             transactions_dict = {}
#
#             te = TransactionN.objects.get(student=temp_user_id)
#             # for _ in te:
#             #	transactions_dict[str(_.date)] = {_.bank : str(_.price)}
#             transactions_dict[str(te.date)] = {te.bank: str(te.price)}
#             data["transactions"] = transactions_dict
#
#             coupons_dict = {}
#
#             cq = CouponN.objects.get(student=temp_user_id)
#             # for _ in cq:
#             #	coupons_dict["is_active"] = str(_.state)
#             #	coupons_dict["food"] = FoodMenuN.objects.get(Key_id = _.food).food_name1
#             #	coupons_dict["self"] = SelfListN.objects.get(self_id = _.self_id).self_name
#
#             coupons_dict["is_active"] = str(cq.state)
#             # coupons_dict["self"] = SelfListN.objects.get(self_id = cq.self_id).self_name
#
#             data["coupons"] = coupons_dict
#
#             return JsonResponse(data)
#         else:
#             return HttpResponse('You are not lgged in')
#     else:
#         return HttpResponse('invalid request')


def get_saturday(date):
    if date.weekday() is 5:
        return date
    elif date.weekday() is 6:
        return date - timedelta(days=1)
    elif date.weekday() is 0:
        return date - timedelta(days=2)
    elif date.weekday() is 1:
        return date - timedelta(days=3)
    elif date.weekday() is 2:
        return date - timedelta(days=4)
    elif date.weekday() is 3:
        return date - timedelta(days=5)
    elif date.weekday() is 4:
        return date - timedelta(days=6)


def week_map():
    ofs = datetime.now().day - datetime.now().weekday() - 1
    bad_ofs = [32, 33, 34, 35, 36, 37, 38]
    a = [_ for _ in range(ofs, ofs + 8)]
    return [element for element in a if element not in bad_ofs]


def week_map1():
    if math.floor(datetime.now().day / 7) == 0:
        return [1, 2, 3, 4, 5, 6]
    elif math.floor(datetime.now().day / 7) == 1:
        return [7, 8, 9, 10, 11, 12, 13]
    elif math.floor(datetime.now().day / 7) == 2:
        return [14, 15, 16, 17, 18, 19, 20]
    else:
        return [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]


def get_week_data():
    sf_data = {}
    s_d = {}

    for _ in week_map():
        try:
            sf_data["price1"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="breakfast")[
                    0].price1
            sf_data["price2"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="breakfast")[
                    0].price2
            sf_data["food_name1"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="breakfast")[
                    0].food_name1
            sf_data["food_name2"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="breakfast")[
                    0].food_name2
            sf_data["key_id"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="breakfast")[
                    0].key_id
            s_d[str(datetime.now().month) + '/' + str(_) + '_breakfast'] = sf_data
            sf_data = {}
        except:
            pass
    for _ in week_map():
        try:
            sf_data["price1"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="lunch")[
                    0].price1
            sf_data["price2"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="lunch")[
                    0].price2
            sf_data["food_name1"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="lunch")[
                    0].food_name1
            sf_data["food_name2"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="lunch")[
                    0].food_name2
            sf_data["key_id"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="lunch")[
                    0].key_id
            s_d[str(datetime.now().month) + '/' + str(_) + '_lunch'] = sf_data
            sf_data = {}
        except:
            pass
    for _ in week_map():
        try:
            sf_data["price1"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="dinner")[
                    0].price1
            sf_data["price2"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="dinner")[
                    0].price2
            sf_data["food_name1"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="dinner")[
                    0].food_name1
            sf_data["food_name2"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="dinner")[
                    0].food_name2
            sf_data["key_id"] = \
                FoodMenuN.objects.all().filter(date__month=datetime.now().month, date__day=_, meal_type="dinner")[
                    0].key_id
            s_d[str(datetime.now().month) + '/' + str(_) + '_dinner'] = sf_data
            sf_data = {}
        except:
            pass
    return s_d


# def get_week_data(data, day):
#     saturday = get_saturday(day)
#     sf_data = {}
#     for _ in range(7):
#         sf_data["price1"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_),
#                                                            meal_type="breakfast").price1
#         sf_data["price2"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_),
#                                                            meal_type="breakfast").price2
#         sf_data["food_name1"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_),
#                                                                meal_type="breakfast").food_name1
#         sf_data["food_name2"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_),
#                                                                meal_type="breakfast").food_name1
#         sf_data["key_id"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_),
#                                                            meal_type="breakfast").credit
#         data[saturday + timedelta(days=_).strftime('%Y/%m/%d') + "/breakfast"] = sf_data
#     for _ in range(7):
#         sf_data["price1"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_), meal_type="dinner").price1
#         sf_data["price2"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_), meal_type="dinner").price2
#         sf_data["food_name1"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_),
#                                                                meal_type="dinner").food_name1
#         sf_data["food_name2"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_),
#                                                                meal_type="dinner").food_name1
#         sf_data["key_id"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_), meal_type="dinner").credit
#         data[saturday + timedelta(days=_).strftime('%Y/%m/%d') + "/breakfast"] = sf_data
#     for _ in range(7):
#         sf_data["price1"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_), meal_type="lunch").price1
#         sf_data["price2"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_), meal_type="lunch").price2
#         sf_data["food_name1"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_),
#                                                                meal_type="lunch").food_name1
#         sf_data["food_name2"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_),
#                                                                meal_type="lunch").food_name1
#         sf_data["key_id"] = FoodMenuN.objects.all().filter(data=saturday + timedelta(days=_), meal_type="lunch").credit
#         data[(saturday + timedelta(days=_)).strftime('%Y/%m/%d') + "/breakfast"] = sf_data


def get_week_coupons(day, std):
    saturday = get_saturday(day)
    data = {}
    try:
        lst = CouponN.objects.filter(
            food__date__gt=datetime.date(saturday.year, saturday.month, saturday.day), student=std)
        i = 0
        coupon = {}
        while i < len(lst):
            coupon["state"] = lst[i].state
            coupon["coupon_id"] = lst[i].coupon_id
            coupon["food_id"] = lst[i].food.key_id
            coupon["food_name1"] = lst[i].food.food_name1
            coupon["food_name2"] = lst[i].food.food_name2
            coupon["price1"] = lst[i].food.price1
            coupon["price2"] = lst[i].food.price2
            coupon["self_name"] = lst[i].self_id.self_name
            data[lst[i].food.date.strftime('%m/%d') + '_' + lst[i].food.meal_type] = coupon
            coupon = {}
    except:
        pass
    return data


# @csrf_exempt
# def self_data(request):
#     '''remove the token and the username for the database'''
#     if request.method == 'GET':
#         return HttpResponse('Post')
#     elif request.method == 'POST':
#         req = request.read()
#         j = json.loads(req)
#         token = j['token']
#         if token_check(token):
#             st = cred.objects.get(token=token)
#             temp_user_id = st.username
#             data = {}
#             get_week_data(data, datetime.now())
#             get_week_coupons(data, datetime.now(), st)
#
#             return JsonResponse(data)
#         else:
#             return HttpResponse('You are not lgged in')
#     else:
#         return HttpResponse('invalid request')


def get_student(sto):
    std = {}
    std["first_name"] = sto.first_name
    std["last_name"] = sto.last_name
    std["student_no"] = sto.student_no
    std["student_type"] = sto.std_type
    std["credit"] = sto.credit
    return std


@csrf_exempt
def self_data(request):
    '''remove the token and the username for the database'''
    if request.method == 'GET':
        return HttpResponse('Post')
    elif request.method == 'POST':
        req = request.read()
        j = json.loads(req)
        token = j['token']
        st = cred.objects.get(token=token)
        temp_user_id = st.username
        std = StudentN.objects.get(student_no=temp_user_id)
        data = {}
        if token_check(token):
            data["self_data"] = get_week_data()
            data["student"] = get_student(std)
            data["coupons"] = get_week_coupons(datetime.now(), std)

            return JsonResponse(data)
        else:
            return HttpResponse('You are not lgged in')
    else:
        return HttpResponse('invalid request')
