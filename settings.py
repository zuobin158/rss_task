#-*- coding:utf-8 -*-

import os
import json
import argparse
import datetime

env = getattr(argparse, 'env')
PROJECT_PATH = os.path.dirname(__file__)
# 上传cc的java文件
UPLOAD_JAR_PATH = os.path.join(PROJECT_PATH, 'lib', 'ccuploader.jar')
# edx提供的rss url
RSS_URL = 'https://www.edx.org/api/v2/report/course-feed/rss'
# rss课程字段和xuetangx的课程字段对应关系,元组第一个代表rss字段，第二个代表默认值(当rss的val为空时使用默认值)
RSS_PACK_COURSE = {
    'course_id': ('course_id', ''),
    'course_num': ('course_code', ''),
    'org': ('course_school', ''),
    'name': ('title', ''),
    'subtitle': ('course_subtitle', ''),
    'create_time': ('course_created',''),
    'start': ('course_start', '0000-00-00 00:00:00'),
    'end': ('course_end', '0000-00-00 00:00:00'),
    'thumbnail': ('course_image-thumbnail', ''),
    'video_thumbnail': ('course_image-banner', ''),
    'effort': ('course_effort', ''),
    'length': ('course_length', ''),
    'prerequisites': ('course_prerequisites', ''),
    'about': ('summary', ''),
    'original_url': ('link', ''),
    'status': ('', -1),
    'run': ('', '-'),
    'modified': ('', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    'serialized': ('', -1),
    'owner': ('', 'edX'),
    'comment_status': ('', 0),
    'classtag': ('', 0),
    'intro_video': ('', ''),
    'quiz': ('', ''),
    'chapters': ('', '')
}

#开发环境相关配置---------------------
if env == 'dev':

    MDB = {
        'host':'192.168.9.189',
        'user':'root',
        'passwd':'',
        'db':'edxapp',
        'sock':'',
        'port':3306
    }
    SDB = {
        'host':'192.168.9.189',
        'user':'root',
        'passwd':'',
        'db':'edxapp',
        'sock':'',
        'port':3306
    }
    DB_CNF = {
        'm':{
            json.dumps(MDB):['edxapp']
        },
        's':{
            json.dumps(SDB):['edxapp']
        },
    }
    DB_NAME = {
        'edxapp':'edxapp'
        }

    # 代理服务器地址
    PROXY_SERVER = '192.168.100.35:808'
    # 下载youtube视频工具地址
    YOUTUBE_PATH = '/usr/local/bin/youtube-dl'
    # java执行程序地址
    JAVA_PATH = '/usr/lib/jvm/jdk1.7.0_51/bin/java'

#生产环境相关配置--------------------------
if env == 'online':

    MDB = {
        'host':'192.168.9.189',
        'user':'root',
        'passwd':'',
        'db':'edxapp',
        'sock':'',
        'port':3306
    }
    SDB = {
        'host':'192.168.9.189',
        'user':'root',
        'passwd':'',
        'db':'edxapp',
        'sock':'',
        'port':3306
    }
    DB_CNF = {
        'm':{
            json.dumps(MDB):['edxapp']
        },
        's':{
            json.dumps(SDB):['edxapp']
        },
    }
    DB_NAME = {
        'edxapp':'edxapp'
        }

    PROXY_SERVER = '10.0.0.235:808'
    YOUTUBE_PATH = '/usr/local/bin/youtube-dl'
    JAVA_PATH = '/usr/lib/jvm/jdk1.7.0_51/bin/java'

