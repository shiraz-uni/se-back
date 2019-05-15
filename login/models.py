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
