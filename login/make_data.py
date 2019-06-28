from secrets import token_hex

from .models import *
import random
import datetime


class MakeData:
    student_list = []
    food_list = []

    def save_data(self):
        i = 0
        while i < len(self.student_list):
            self.student_list[i].save()
            i += 1
        i = 0
        while i < len(self.food_list):
            self.food_list[i].save()
            i += 1

    def make_student(self):
        studentFName = ['حمید', 'حسن', 'محمد', 'علی', 'احمد', 'ایمان']
        studentLName = ['عباسی', 'علیزاده', 'محمدی', 'حسنی', 'صفری', 'سهیلی']
        stdType = ['خوابگاهی', 'غیر خوابگاهی']
        stdCredit = [0, 7000, 30000, 5000, 7525, 5120]

        for _ in range(6):
            self.student_list.append(StudentN(first_name=studentFName[_], last_name=studentLName[_],
                                              student_no="100" + str(_), std_type=stdType[_ % 2], credit=stdCredit[_],
                                              password='123'))

    self_list = ['غذاخوري ارم', 'غذاخوري دانشكده مهندسي نفت و گاز', 'رستوران کوهپايه', 'رستوران بيرون برآسمان']

    def make_food(self):
        foodName1 = ['استامبولي پلو با مرغ خلال با ماست و موسير', 'چلو خورشت بادمجان با ماست و موسير',
                     'زرشك پلو با مرغ با ماست', 'عدس پلو با گوشت با ماست و موسير', 'چلو خورشت سبزي با ماست و موسير',
                     'چلو جوجه كباب با دوغ', ' چلو كباب كوبيده و گوجه با دلستر']
        foodName2 = ['خوراک املت با عدسي', 'خوراك كوكو سيب زميني با سوپ جو', 'خوراک مرغ بندري با سوپ ورميشل',
                     'خوراک فلافل با آش ماست', 'خوراک کوفته بادمجان با دال عدس', 'خوراك كتلت با يتيمک کدو و خيارشور',
                     'خوراک شکاري مرغ با سوپ ورميشل']
        foodName3 = ['نون پنیر', 'املت', 'نون مربا', 'نون شکلات']

        price = [1500, 750, 1350]

        for _ in range(21):
            a = random.randint(0, 6)
            b = random.randint(0, 6)
            while b == a:
                b = random.randint(0, 6)
            c = random.randint(0, 3)
            d = random.randint(0, 3)
            while d == c:
                d = random.randint(0, 3)

            self.food_list.append(
                FoodMenuN(key_id=token_hex(8), price1=price[random.randint(0, 2)], price2=price[random.randint(0, 2)],
                          food_name1=foodName1[a], food_name2=foodName1[b],
                          date=datetime.datetime.now() + datetime.timedelta(days=_), meal_type='lunch'))

            self.food_list.append(
                FoodMenuN(key_id=token_hex(8), price1=price[random.randint(0, 2)], price2=price[random.randint(0, 2)],
                          food_name1=foodName2[a], food_name2=foodName2[b],
                          date=datetime.datetime.now() + datetime.timedelta(days=_), meal_type='dinner'))

            self.food_list.append(
                FoodMenuN(key_id=token_hex(8), price1=price[random.randint(0, 2)], price2=price[random.randint(0, 2)],
                          food_name1=foodName3[c], food_name2=foodName3[d],
                          date=datetime.datetime.now() + datetime.timedelta(days=_), meal_type='breakfast'))
