# Generated by Django 2.2.1 on 2019-05-24 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cred',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('ti', models.FloatField()),
                ('token', models.CharField(max_length=50)),
            ],
        ),
    ]
