#-*- coding:utf-8 -*-

import os
import argparse
import logging

# 设置全局的环境参数env
parser = argparse.ArgumentParser() 
parser.add_argument('-env', help="display the env is dev or online", type=str)    
parser.add_argument('-debug', help="debug mode, True or False", type=bool)    
parser.set_defaults(env='dev')
parser.set_defaults(debug=True)
setattr(argparse, 'env', parser.parse_args().env)
setattr(argparse, 'debug', parser.parse_args().debug)

# 设置log输出格式
PATH = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.DEBUG,
            format='[%(levelname)s]%(asctime)s %(filename)s[method:%(funcName)s, line:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=PATH + '/project.log',
            filemode='a')
