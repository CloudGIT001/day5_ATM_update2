#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen


import os
from core import db_handler
from conf import settings
from core import logger
from core import accounts
import json
import time
import datetime


def acc_auth(account, password):
    global new_user
    db_path = db_handler.db_handler(settings.DATABASE_SHOP)
    account_file = "%s/%s.json" % (db_path, account)

    if os.path.isfile(account_file):
        new_user = False

        with open(account_file, 'r') as f:
            account_data = json.load(f)
            if account_data['password'] == password:
                return account_data
            else:
                print("\033[31;1m登陆密码输入错误~\033[0m")
    else:
        new_user = True

        print("该用户ID不存在，请注册~")


def acc_login(user_data, log_obj):
    retry_count = 0
    same_user_count = 0
    last_user = ""

    while user_data['is_authenticated'] is not True and retry_count < 3:
        user = input("\033[32;1m\033[32;1m登录用户名>>>\033[0m:").strip()
        password = input("\033[32;1m用户登陆密码>>>\033[0m:").strip()
        if last_user == user:
            same_user_count += 1
        auth = acc_auth(user, password)
        if auth:
            user_data['is_authenticated'] = True
            user_data['user'] = user
            money = auth["balance"]
            old_money = money
            return auth
        last_user = user
        retry_count += 1
    else:
        print(same_user_count)
        if same_user_count == retry_count - 1:
            log_obj.error("account [%s] too many login attempts"%last_user)
        exit()


def sign_up(user_data):
    exist_flag = True
    while exist_flag is True:
        user = input("\033[32;1m注册用户ID>>>\033[0m:").strip()
        password = input("\033[32;1m用户密码>>>\033[0m:").strip()
        exist_flag = acc_check(user)
        if exist_flag:
            print("用户ID已经存在，请注册其他用户ID")
            exist_flag = True
            continue
        else:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            account_data = {"enroll_date": today, "balance": 10000, "password": password, "user": user, "status": 0}
            accounts.dump_shop_account(account_data)
            user_data['is_authenticated'] = True
            user_data['user'] = user
            user_data['account_data'] = account_data
            print("\033[33;1m用户信息注册成功\033[0m".center(50, "-"))
            time.sleep(2)
            print("\n\033[32;1m欢迎来到购物商城，祝购物愉快~\033[0m\n")
            return True


def acc_check(account):
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account)
    if os.path.isfile(account_file):
        with open(account_file, 'r') as f:
            account_data = json.load(f)
            return account_data