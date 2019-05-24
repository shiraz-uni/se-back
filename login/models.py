from django.db import models

# Create your models here.
class Student(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    studentNo = models.CharField(max_length=20, primary_key=True)
    major = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    coupons = models.IntegerField()
    credit = models.FloatField()
    password = models.CharField(max_length=50)


class Coupon(models.Model):
    price = models.FloatField()
    date = models.DateField()
    selfname = models.CharField(max_length=100)
    food = models.ForeignKey('Food', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)


class Transaction(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    price = models.FloatField()
    bank = models.CharField(max_length=100)
    date = models.DateField()
    type = models.DateField(max_length=20)


class Food(models.Model):
    name = models.CharField(max_length=20)

class cred(models.Model):
    username = models.CharField(max_length=20)
    ti = models.FloatField()
    token = models.CharField(max_length=50)


class StudentN(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    student_no = models.CharField(max_length=100, primary_key=True)
    std_type = models.CharField(max_length=20)
    credit = models.IntegerField()
    password = models.CharField(max_length=50)


class CouponN(models.Model):
    coupon_id = models.CharField(max_length=100, primary_key=True)
    state = models.BooleanField()
    food = models.ForeignKey('FoodMenuN', on_delete=models.CASCADE)
    student = models.ForeignKey('StudentN', on_delete=models.CASCADE)
    self = models.ForeignKey('SelfListN', on_delete=models.CASCADE)


class TransactionN(models.Model):
    student = models.ForeignKey('StudentN', on_delete=models.CASCADE)
    price = models.IntegerField()
    bank = models.CharField(max_length=100)
    date = models.DateField()


class SelfListN(models.Model):
    self_id = models.CharField(max_length=100, primary_key=True)
    self_name = models.CharField(max_length=20)


class FoodMenuN(models.Model):
    key_id = models.CharField(max_length=100, primary_key=True)
    price1 = models.FloatField()
    price2 = models.FloatField()
    food_name1 = models.CharField(max_length=50, null=True)
    food_name2 = models.CharField(max_length=50, null=True)
    date = models.DateField()
    meal_type = models.CharField(max_length=20)  # sobhane nahar sham