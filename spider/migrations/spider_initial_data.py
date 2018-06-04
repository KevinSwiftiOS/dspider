# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-10 02:14


from django.db import migrations

from spider.driver.travel.core.traveldriver import WEBSITE_NAME_LIST,DATASOURCE_NAME_LIST

def InitDataWebsite(apps, schema_editor):
    print('InitDataWebsite')
    model = apps.get_model("spider", "DataWebsite")
    db_alias = schema_editor.connection.alias
    data_list = []
    for data in WEBSITE_NAME_LIST:
        data_list.append(model(name=data))
        print(data)
    model.objects.using(db_alias).bulk_create(data_list)

def InitDataSource(apps, schema_editor):
    print('InitDataSource')
    model= apps.get_model("spider", "DataSource")
    db_alias = schema_editor.connection.alias
    data_list = []
    for data in DATASOURCE_NAME_LIST:
        data_list.append(model(name=data))
        print(data)
    model.objects.using(db_alias).bulk_create(data_list)

class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(InitDataWebsite),
        migrations.RunPython(InitDataSource),
    ]