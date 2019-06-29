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
import datetime


def compare_date(d, dt):
    """1 if first is bigger, 0 for equal and -1 for less"""
    # parsed = date_str.split('-')
    # db_year = int(parsed[0])
    # db_month = int(parsed[1])
    # db_day = int(parsed[2])
    # return datetime(year=db_year, month=db_month, day= db_day)
    if d.year > dt.year:
        return 1
    elif d.year == dt.year and d.month > dt.month:
        return 1
    elif d.year == dt.year and d.month == dt.month and d.day > dt.day:
        return 1
    elif d.year == dt.year and d.month == dt.month and d.day == dt.day:
        return 0
    else:
        return -1


def credit_change(change, student):
    try:
        # student = StudentN.objects.get(student_no=id)
        student.credit = student.credit + int(change)
        student.save()
    except:
        return


def cridentials_test(user, password):
    c = None
    cc = None
    try:
        c = StudentN.objects.get(student_no=user)
    except:
        return False
    try:
        cc = cred.objects.get(username=user)
    except:
        cc = None
        temp = 1
    finally:
        if c is not None and c.password == password and cc is None:
            return True
        else:
            return False


def token_check(token):
    try:
        st = cred.objects.get(token=token)
        if st is not None:
            return True
        else:
            return False
    except:
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

        # only for testing
        if (token == 'N'):
            try:
                username_out = j['username']
                st = cred.objects.get(username=username_out)
                if st is not None:
                    st.delete()
                    return HttpResponse("OK")
                else:
                    return HttpResponse('You are not lgged in')
            except:
                return HttpResponse("Wrong credentials")

        elif token_check(token):
            try:
                st = cred.objects.get(token=token)
                if st is not None:
                    st.delete()
                    return HttpResponse("OK")
                else:
                    return HttpResponse('You are not lgged in')
            except:
                return HttpResponse("Wrong credentials")
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


# def week_map():
#     ofs = datetime.datetime.now().weekday()
#     ofsm = datetime.datetime.now().day - (7 - ofs)
#     bad_ofs = [32, 33, 34, 35, 36, 37, 38]
#     a = [_ for _ in range(ofsm, ofs + 8)]
#     return [element for element in a if element not in bad_ofs]


def get_week_data():
    sf_data = {}
    s_d = {}
    saturday = datetime.datetime.now() + timedelta(days=1)

    for _ in range(7):
        try:
            sf_data["price1"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="breakfast")[
                    0].price1
            sf_data["price2"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="breakfast")[
                    0].price2
            sf_data["food_name1"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="breakfast")[
                    0].food_name1
            sf_data["food_name2"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="breakfast")[
                    0].food_name2
            sf_data["key_id"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="breakfast")[
                    0].key_id
            s_d['2019/' + (saturday + timedelta(days=_)).strftime('%m/%d') + '_breakfast'] = sf_data
            sf_data = {}
        except:
            pass
    for _ in range(7):
        try:
            sf_data["price1"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="lunch")[
                    0].price1
            sf_data["price2"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="lunch")[
                    0].price2
            sf_data["food_name1"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="lunch")[
                    0].food_name1
            sf_data["food_name2"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="lunch")[
                    0].food_name2
            sf_data["key_id"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="lunch")[
                    0].key_id
            s_d['2019/' + (saturday + timedelta(days=_)).strftime('%m/%d') + '_lunch'] = sf_data
            sf_data = {}
        except:
            pass
    for _ in range(7):
        try:
            sf_data["price1"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="dinner")[
                    0].price1
            sf_data["price2"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="dinner")[
                    0].price2
            sf_data["food_name1"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="dinner")[
                    0].food_name1
            sf_data["food_name2"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="dinner")[
                    0].food_name2
            sf_data["key_id"] = \
                FoodMenuN.objects.all().filter(date__month=(saturday + timedelta(days=_)).month,
                                               date__day=(saturday + timedelta(days=_)).day, meal_type="dinner")[
                    0].key_id
            s_d['2019/' + (saturday + timedelta(days=_)).strftime('%m/%d') + '_dinner'] = sf_data
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
        lst = CouponN.objects.filter(student=std)
        i = 0
        coupon = {}
        while i < len(lst):

            if compare_date(lst[i].food.date, saturday) > -1:
                coupon["state"] = lst[i].state
                coupon["coupon_id"] = lst[i].coupon_id
                coupon["food_id"] = lst[i].food.key_id
                coupon["food_name1"] = lst[i].food.food_name1
                coupon["food_name2"] = lst[i].food.food_name2
                coupon["price1"] = lst[i].food.price1
                coupon["price2"] = lst[i].food.price2
                coupon["self_name"] = lst[i].self_id.self_id
                coupon["self"] = lst[i].self_id.self_name
                data['2019/' + lst[i].food.date.strftime('%m/%d') + '_' + lst[i].food.meal_type] = coupon
                coupon = {}
            i += 1
    except:
        pass
    return data


def delete_coupon(coupon_id, std):
    try:
        clist = []
        coupon = CouponN.objects.get(coupon_id=coupon_id)
        clist.append(coupon)
        if int(clist[0].student.student_no) == int(std.student_no):
            if int(coupon.state):
                credit_change(coupon.food.price1, coupon.student)
            else:
                credit_change(coupon.food.price2, coupon.student)
            coupon.delete()
        else:
            return -1
    except Exception as e:
        return ('Failed to upload to ftp: ' + str(e))


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
        try:
            st = cred.objects.get(token=token)
            temp_user_id = st.username
            std = StudentN.objects.get(student_no=temp_user_id)
            data = {}
            if token_check(token):
                data["self_data"] = get_week_data()
                data["student"] = get_student(std)
                data["coupons"] = get_week_coupons(datetime.datetime.now(), std)

                return JsonResponse(data)
            else:
                return HttpResponse('You are not logged in')
        except Exception as e:
            return HttpResponse('Something went wrong ' + str(e))
    else:
        return HttpResponse('invalid request')


@csrf_exempt
def delete(request):
    if request.method == 'GET':
        return HttpResponse('Post')
    elif request.method == 'POST':
        req = request.read()
        j = json.loads(req)
        token = j['token']
        coupon = j['coupon_id']
        try:
            st = cred.objects.get(token=token)
            temp_user_id = st.username
            std = StudentN.objects.get(student_no=temp_user_id)
            data = {}
            if token_check(token):
                data["status"] = "deleted"
                if delete_coupon(coupon, std) == -1:
                    temp_d = {}
                    temp_d['status'] = "Wrong Credential"
                    return JsonResponse(temp_d)
                else:
                    return JsonResponse(data)
            else:
                return HttpResponse('You are not logged in')
        except:
            return HttpResponse('You are not logged in')
    else:
        return HttpResponse('invalid request')


@csrf_exempt
def purchase(request):
    if request.method == 'GET':
        return HttpResponse('Post')
    elif request.method == 'POST':
        req = request.read()
        j = json.loads(req)
        token = j['token']
        food_id = j['food_id']
        state = j['state']
        self_id = j['self']
        try:
            st = cred.objects.get(token=token)
            temp_user_id = st.username
            std = StudentN.objects.get(student_no=temp_user_id)
            try:
                food = FoodMenuN.objects.get(key_id=food_id)

            except:
                temp_dd = {}
                temp_dd['status'] = "No Food"
                return JsonResponse(temp_dd)
            try:
                self = SelfListN.objects.get(self_id=self_id)

            except:
                temp_ddd = {}
                temp_ddd['status'] = "No Self"
                return JsonResponse(temp_ddd)

            coupon_id = secrets.token_hex(8)
            data = {}
            datatt = {}
            datattt = {}
            if token_check(token) and food is not None and self is not None:
                data["status"] = "purchased"
                if (food.meal_type != "lunch" and std.std_type == "غیر خوابگاهی"):
                    datatt["status"] = "you can't buy this type of meal"
                    return JsonResponse(datatt)
                if ((int(state) == 1 and std.credit < food.price1) or (int(state) != 1 and std.credit < food.price2)):
                    datattt['status'] = "you don't have enough credit"
                    return JsonResponse(datattt)
                CouponN(coupon_id=coupon_id, state=state, food=food, student=std, self_id=self).save()
                if int(state):
                    credit_change(-food.price1, std)
                else:
                    credit_change(-food.price2, std)
                return JsonResponse(data)
            else:
                return HttpResponse('You are not logged in')
        except:
            return HttpResponse('You are not logged in')
    else:
        return HttpResponse('invalid request')

def stat(request):
    st = cred.objects.all()
    val_em = (len(st)/150)*100
    em_str = '''

    <!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" />
  <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600&amp;subset=latin-ext" rel="stylesheet">
  <title>CE PROJECT</title>
  <style>
  html {
  width: 100%;
  height: 100%;
}

/* Width and height are needed for some elements to work properly */
body {
  width: 100%;
  height: 100%;
  color: #555555;
  background-color: #000000;
  font-family: "Source Sans Pro";
  text-rendering: optimizeSpeed !important;
  /* text-shadow: 2px 1px 3px #444444; */
}

.background {
    background: url(http://i.imgur.com/UJJu1ho.jpg);
    background-repeat: no-repeat;
    background-attachment: scroll;
    background-size: cover;
    background-position: center;
    min-width: 100%;
    min-height: 100%;
    z-index: -1;
    position: absolute;
    margin: 0;
    top: 0;
    left: 0;
    padding: 0;
    border: 0;
    animation: kenburns 110s infinite linear;
  }

.hover-underline a {
  text-decoration: none !important;
  position: relative;
}

.hover-underline a::after {
  content: "";
  position: absolute;
  top: calc(100%);
  left: 50%;
  right: 50%;
}

.hover-underline a:hover::after {
  left: 0;
  right: 0;
  transition-property: left, right;
  transition-duration: 0.5s;
  transition-timing-function: ease;
  border-bottom: 0.125rem solid #fefefe;
}

/* Turning off decorations, e.g. underline for links */
.no-deco {
  text-decoration: none !important;
}

.icon-pad-right {
  padding-right: 0.3em;
}

.footer-text {
  font-size: 0.8rem;
}

.scaling-font {
  font-size: calc(3rem + 1vw);
  font-weight: 600;
  line-height: calc(5rem + 1vw);
}

.page-bottom {
  position: fixed;
  right: 15px;
  bottom: 1vh;
  left: 15px;
  z-index: 1000;
}

.pad-top {
  padding-top: 15px;
}

.center {
  position: fixed;
  margin: 0;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Rotate is needed for IE, otherwise it is jumpy */
@keyframes kenburns {
  50% {
    transform: scale(1.3) rotate(0.04deg);
  }
}
  </style>
</head>

<body>
  <div style="height: 100%">
    <div class="container-fluid" style="height: 100%; overflow: hidden">
      <div class="background"></div>
      <div class="row">
        <div class="col-12 text-right hover-underline pad-top">
          <h1>

          </h1>
        </div>
      </div>
      <!-- Width must be defined for centered text in IE -->
      <div class="row center" style="width: 100%">
        <div class="col-12 text-white text-center">
          <h1 class="scaling-font" style="overflow:hidden"> ''' + str(val_em)[:4] + '''  PERCENT SERVERLOAD</h1>
        </div>

      </div>
      <div class="row page-bottom footer-text">
        <div class="col-12 text-center hover-underline">
          <a class="text-white"><i class="fa fa-camera icon-pad-right"></i>CE PROJECT</a>
        </div>
      </div>
    </div>

  </div>
</body>

</html>

    '''
    return HttpResponse(em_str)
