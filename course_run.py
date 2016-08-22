#-*- coding:utf-8 -*-

import __init__
from course import CourseService


def run():
    # 保存课程信息
    CourseService().save_course()

if __name__ == '__main__':
    run()
