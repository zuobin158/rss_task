# -*- coding: utf-8 -*-

'''
Copyright (c) 2015,xuetangx
All rights reserved.

摘    要: course.py rss课程的相关操作
创 建 者: ZuoBin
创建日期: 2015-05-08
'''

import logging

from rss import Rss
from lib.database import trans
from util import convert_str
from settings import (
    RSS_URL, 
    RSS_PACK_COURSE
)
from model import (
    Course, 
    CourseRss,
    CourseOrg,
    CourseStaff,
    CourseMStaff
)


class CourseService(object):

    def save_course(self):
        '''从rss上获取课程信息并解析保存。
        '''
        course_list = Rss(url=RSS_URL).parse_rss_content()
        for course in course_list:
            try:
                self._save_single_course(course)
            except Exception, e:
                logging.error('Error is %s' % e, exc_info=True)

    @trans(Course)
    def _save_single_course(self, course):
        '''保存单个课程信息
        Args:
           course: rss课程信息 
        '''
        if self._check_course_exist(course):
            logging.info('课程id为%s 的课程已经存在!' % convert_str(course.course_id))
            return convert_str(course.course_id)
        # 保存课程信息
        co = self._pack_course(course)
        cr_id = co.save().course_id
        # 保存rss课程下载信息
        self._save_course_rss(cr_id, course)
        # 保存大学信息
        org_id = self._save_college(course)
        # 保存老师信息
        tid = self._save_teacher(course, org_id)
        # 保存课程和老师的对应关系
        self._save_course_m_teacher(co.id, tid)
        return cr_id

                
    @staticmethod            
    def _check_course_exist(course):
        '''检查该课程是否已经存在
        '''
        course_id = convert_str(course.course_id)
        c = Course.mgr().Q().filter(course_id=course_id)[0]
        return True if c else False
        
    @staticmethod
    def _pack_course(course):
        '''封装course对象，转换字段
        Args:
           course: rss课程信息
        Returns:
           课程信息的model实体
        '''
        co = Course.new()
        for attr in co._fields:
            if attr in RSS_PACK_COURSE:
                # 如果在配置的对应关系中则用其val，如果不在或者取到的值为空则用默认值
                if RSS_PACK_COURSE[attr][0]:
                    val = getattr(course, RSS_PACK_COURSE[attr][0])
                    val = convert_str(val) 
                    if not val:
                        val = RSS_PACK_COURSE[attr][1]
                else:
                    val = RSS_PACK_COURSE[attr][1]
                setattr(co, attr, val) 
        return co
    
    @staticmethod
    def _save_course_rss(cr_id, course):
        '''保存rss课程信息
        Args:
           cr_id: 课程id，唯一标示
           course: rss课程信息
        '''
        cr = CourseRss.new()
        cr.course_id = cr_id
        val = getattr(course, 'course_video-youtube')
        cr.video_url = convert_str(val)
        cr.save()

    @staticmethod
    def _save_college(course):
        '''保存大学信息
        Args:
            course: 课程信息
        Returns:
           大学id
        '''
        org = convert_str(course.course_school)
        college = CourseOrg.mgr().Q().filter(org=org)[0]
        if college:
            return college.id
        new_college = CourseOrg.new()
        new_college.org = org
        new_college.name = ''
        new_college.about = ''
        org_id = new_college.save().id
        return org_id

    @staticmethod
    def _save_teacher(course, org_id):
        '''
        Args:
            course: 课程信息
            org_id: 所属大学id
        Returns:
            老师id
        '''
        staff_name = convert_str(course.staff_name)
        teacher = CourseStaff.mgr().Q().filter(name=staff_name)[0]
        if teacher:
            return teacher.id
        staff = CourseStaff.new()
        staff.name = staff_name
        staff.org_id_id = org_id
        staff.company = convert_str(course.course_school)
        staff.department = ''
        staff.position = ''
        staff.avartar = convert_str(course.staff_image)
        staff.about = convert_str(course.staff_bio)
        sid = staff.save().id
        return sid

    @staticmethod
    def _save_course_m_teacher(cid, tid):
        '''保存课程和老师对应关系
        Args:
            cid: 课程id
            tid: 老师id
        '''
        cms = CourseMStaff.mgr().Q().filter(staff_id=tid, course_id=cid)[0]
        if cms:
           return
        cs = CourseMStaff.new()
        cs.staff_id = tid
        cs.course_id = cid
        cs.role = 0
        cs.save()

if __name__ == '__main__':
    CourseService().save_course()
    
