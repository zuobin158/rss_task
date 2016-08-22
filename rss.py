# -*- coding: utf-8 -*-

'''
Copyright (c) 2015,xuetangx
All rights reserved.

摘    要: rss.py
创 建 者: ZuoBin
创建日期: 2015-05-08
'''

import logging
import feedparser


class Rss(object):

    def __init__(self, url=None):
        self.url = url

    def get_rss_content(self):
        '''
        通过rss获取订阅内容
        '''
        try:
            if self.url:
                res = feedparser.parse(self.url)
                return res     
        except Exception, e:
            logging.error('Error is %s'% e, exc_info=True)
        return ''

    def parse_rss_content(self):
        '''
        获取rss的内容，封装list
        '''
        content = self.get_rss_content()
        course_list = []
        if content.entries:
            for item in content.entries:
                course_list.append(item)
        return course_list

if __name__ == '__main__':
    pass
    
