# -*- coding: utf-8 -*-               

'''
Copyright (c) 2015,xuetangx
All rights reserved.

摘    要: util.py
创 建 者: ZuoBin
创建日期: 2015-05-08
'''


import datetime
from dateutil import parser


def convert_date(da):
    '''日期格式转换
    '''
    try:
        dd = parser.parse(da)
        res = dd.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError, e:
        res = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return res

def convert_str(val):
    '''把unicode字符转换成utf-8
    '''
    if val and isinstance(val, unicode):
        val = val.encode('utf-8')
    return val

