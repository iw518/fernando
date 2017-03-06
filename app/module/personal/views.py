#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2016-12-13
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask import render_template, redirect, url_for, flash, request,session
from app.models import Project, Registration, Team
from . import personal
from .forms import UserForm
from app.models import User
import json
from functools import reduce

@personal.route('/', methods=['POST', 'GET'])
def index():
    form = UserForm()
    if request.method == "GET":
        return render_template('personal/index.html', form=form)

    elif request.method == 'POST':
        user_id = session["user_id"]
        # user_id = request.form['user_selections']
        user = User.query.filter_by(id=user_id).first()
        projects = user.find_projects()
        data = []
        for project in projects:
            fee_contract_sum=0
            fee_income_sum=0
            fee_income_sum_real=0
            fee_income_real_list=[]
            fund_contract_sum=project.profile.fund_contract_sum
            fund_income_sum=project.profile.fund_income_sum

            if not (fund_contract_sum is None):
                fee_contract_sum=round(pow(10,4)*fund_contract_sum*fee_K(pow(10,4)*fund_contract_sum),0)
            if not (fund_income_sum is None):
                fee_income_sum = round(pow(10,4)*fund_income_sum*fee_K(pow(10,4)*fund_income_sum),0)
                fee_income_sum_real=reduce(lambda x,y : x + y,[techfee.fee_income for techfee in project.techfees],0)
                fee_income_real_list=[(techfee.fee_income,techfee.income_date.strftime("%Y/%m/%d")) for techfee in project.techfees]
            data.append({"id": project.id,
                         "nickname": project.nickname,
                         "fullname": project.fullname,
                         "fund_contract_sum": fund_contract_sum,
                         "fund_income_sum": fund_income_sum,
                         "fee_contract_sum": fee_contract_sum,
                         "fee_income_sum":fee_income_sum,
                         "fee_income_sum_real":fee_income_sum_real,
                         "fee_income_real_list":fee_income_real_list
                         })
            if project.profile.filed > 0:
                data[-1]["filed"] = "是"
                data[-1]["filed_date"] = str(project.profile.filed_date)
            else:
                data[-1]["filed"] = "否"
                data[-1]["filed_date"] = ""
        # print(data)
        return json.dumps(data)

def fee_K(income):
    K=0
    if income > 0 and income<= (1*pow(10,5)):
        K = 4.00
    elif income >(1*pow(10,5)) and income<= (5*pow(10,5)):
        K = 4.00-3.75*(income*pow(10,-6)-0.1)
    elif income > (5*pow(10,5)) and income< (10*pow(10,5)):
        K = 2.50-2.00*(income*pow(10,-6)-0.5)
    elif income >= (10*pow(10,5)):
        K = 1.50
    return round(K, 2)*0.01