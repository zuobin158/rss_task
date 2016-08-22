# -*- coding: utf-8 -*-

'''
Copyright (c) 2015,xuetangx
All rights reserved.

摘    要: model.py
创 建 者: ZuoBin
创建日期: 2015-05-12
'''

import datetime

from settings import DB_NAME
from lib.database import Model
from util import convert_date


class Course(Model):
    '''
    课程信息
    '''
    _db = DB_NAME["edxapp"]
    _table = 'course_meta_course'
    _pk = 'id'
    _fields = set(['id', 'status', 'course_id', 'course_num', 'org', 'name',
                   'run', 'subtitle','create_time', 'modified', 'enrollment_start',
                   'enrollment_end', 'start', 'end', 'intro_video', 'thumbnail',
                   'video_thumbnail', 'effort', 'length', 'quiz', 'prerequisites',
                   'about', 'chapters', 'serialized', 'owner', 'original_url',
                   'keywords', 'comment_org', 'comment_course', 'comment_status',
                   'classtag'
                 ])

    def before_add(self):
        self.create_time = convert_date(self.create_time)

    def before_update(self):
        pass
        
    def get_course_by_id(self, course_id):
        course = self.Q().filter(id=course_id)[0]
        return course
        
class CourseRss(Model):
    '''rss同步课程信息
    '''
    _db = DB_NAME["edxapp"]
    _table = 'course_rss'
    _pk = 'id'
    _fields = set(['id', 'course_id', 'ccid', 'create_time', 'upload_time',
                   'video_id', 'video_url'
                 ])

    def before_add(self):
        self.create_time = datetime.datetime.now()

class CourseOrg(Model):
    '''大学信息
    '''
    _db = DB_NAME["edxapp"]
    _table = 'course_meta_organization'
    _pk = 'id'
    _fields = set(['id', 'org', 'name', 'about'])


class CourseStaff(Model):
    '''老师信息
    '''
    _db = DB_NAME["edxapp"]
    _table = 'course_meta_staff'
    _pk = 'id'
    _fields = set(['id', 'name', 'org_id_id', 'company', 'department',
                   'position', 'avartar', 'about', 'mailing_address'
                 ])


class CourseMStaff(Model):
    '''课程和老师的对应关系
    '''
    _db = DB_NAME["edxapp"]
    _table = 'course_meta_coursestaffrelationship'
    _pk = 'id'
    _fields = set(['id', 'staff_id', 'course_id', 'role'])


