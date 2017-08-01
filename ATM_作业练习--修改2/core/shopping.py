#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen


from core import auth_shop
from core import logger
from core import accounts
from conf import settings
from conf import goods
import time
import os
import subprocess


access_logger = logger.logger('access')
shopping_cart = {}
all_cost = 0

user_data = {
    'is_authenticated': False,
    'account_data': None
}


def interactive():
    menu = """
    -*-*-*-*-*-*- 购物商城 -*-*-*-*-*-*-\033[32;1m
    0. 退出程序
    1. 登录商城
    2. 注册帐号
    \033[0m"""
    menu_dict = {
        '1': 'login()',
        '2': 'auth_shop.sign_up(user_data)',
        '0': 'logout()'
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input("请选择操作[0=exit]>>>:").strip()
        if user_option in menu_dict.keys():
            exit_flag = eval(menu_dict[user_option])  #将字符串str当成有效的表达式来求值并返回计算结果
        else:
            print("\033[31;1m操作错误~\033[0m")


def login():
    acc_data = auth_shop.acc_login(user_data, access_logger)  # 登录验证
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        return True


def logout():
    exit("\n\033[31;1m------------- 退出成功 -------------\033[0m")


def show_shopping_cart(user_data, all_cost):
    if user_data['is_authenticated'] is True:
        account_data = user_data['account_data']  # 用户信息
        money = account_data['balance']

        print("购物车商品列表：")
        print("%-20s %-15s %-10s %-20s" % ("商品", "价格", "数量", "总价"))
        for key in shopping_cart:
            p_name = key[0]
            p_price = int(key[1])
            p_number = int(shopping_cart[key])
            print("%-20s %-15s %-10s \033[32;1m%-20s\033[0m" % (p_name, p_price, p_number, p_price * p_number))
        print("%-20s %-15s %-10s \033[32;1m%-20s\033[0m" % ("购物车列表:", "", "", all_cost))
        print("余额还剩 [\033[32;1m%s\033[0m]" % money)
        accounts.dump_shop_account(account_data)


def show_shopping_history(user_name, log_type):
    log_file = "%s/log/%s_%s" % (settings.BASE_DIR, user_name, settings.LOG_TYPES[log_type])
    pass
    # if os.path.getsize(log_file):
    #     logger.show_log(user_name, log_type)


def charge_money(money):
    input("\033[41;1m金额充值功能未实现，按任意键结束~\033[0m")
    exit()


def go_shopping(log_obj,user_data):
    flag = True
    while flag:
        account_data = user_data['account_data']
        money = account_data['balance']
        global all_cost
        product_list = []
        print ("\033[34;1mProduct List\033[0m".center(50,"-"))
        for index,item in enumerate(goods.menu):
            print("%d --> %s" % (index, item))
            product_list.append(item)
        print("小提示：\033[32;1mq=[退出]；t=[充值账户];c=[打印购物车]\033[0m")

        user_choice = input("请选择操作内容[q=quit]>>>:").strip()
        if user_choice.isdigit():
            user_choice = int(user_choice)
            if 0 <= user_choice < len(goods.menu):
                # print("---->Enter \033[32;1m%s\033[0m" % (product_list[user_choice]))
                product_number = input("请输入购买数量:").strip()
                if product_number.isdigit():
                    product_number = int(product_number)
                    p_item = product_list[user_choice]
                    p_name = p_item[0]
                    p_price = int(p_item[1])
                    new_added = {}

                    if p_price * product_number <= money:
                        new_added = {p_item: product_number}
                        for k, v in new_added.items():
                            if k in shopping_cart.keys():
                                shopping_cart[k] += v
                            else:
                                shopping_cart[k] = v

                        money -= p_price * product_number
                        all_cost += p_price * product_number
                        log_obj.info("account:%s action:%s product_number:%s goods:%s cost:%s"
                                     %(account_data['user'], "shopping", product_number, p_name, all_cost))
                        print("以添加 [\033[32;1m[%d]\033[0m [\033[32;1m%s\033[0m] 到购物车,"
                              "你的余额还剩 [\033[32;1m%s\033[0m]" % (product_number, p_name, money))
                        time.sleep(1)
                        continue


                    else:
                        print("\033[41;1m余额不族，不能购买该产品~\033[0m")
                        continue

                else:
                    print("\033[31;1m输入错误~\033[0m")
            else:
                print("\033[31;1m输入错误，请重新输入\033[0m")
        else:
            if user_choice == "q":
                time.sleep(0.1)
                exit("再见".center(36, "-"))

            if user_choice == "c":
                show_shopping_cart(user_data, all_cost)

            elif user_choice == "t":
                account_data = user_data['account_data']
                money = account_data['balance']
                money = charge_money(money)
                user_data['account_data']['balance'] = money


def shop_run():
    interactive()

    account_data = user_data['account_data']
    user_name = account_data['user']

    log_type = "shopping"
    shopping_logger = logger.logger(log_type, user_name)
    show_shopping_history(user_name, log_type)
    go_shopping(shopping_logger, user_data)


