# -*- coding: utf-8 -*-

'''
Copyright (c) 2015,xuetangx
All rights reserved.

摘    要: test_courses.py 课程相关单元测试
创 建 者: ZuoBin
创建日期: 2015-05-15
'''

import os
import sys
import unittest
import random
import __init__

from settings import RSS_URL
from model import Course
from rss import Rss
from course import CourseService


class CoursesTest(unittest.TestCase):
    
    def setUp(self):
        self.rss_url = RSS_URL
        self.seq = range(100)
        self.cs = CourseService()
        
    def test_parse_rss_content(self):
        '''测试rss接口课程数据
        '''
        course_list = Rss(url=self.rss_url).parse_rss_content()
        self.assertIsInstance(course_list, list)
        self.assertIsNotNone(course_list)

    def test_save_single_course(self):
        '''测试保存单个课程信息
        '''
        element = random.choice(self.seq)
        course_list = Rss(url=self.rss_url).parse_rss_content()
        course = course_list[element]
        course_id = self.cs._save_single_course(course)
        cc = Course.mgr().Q().filter(course_id=course_id)
        self.assertIsNotNone(cc)
        
if __name__ == '__main__':
    unittest.main()

