#-*- coding:utf-8 -*-

'''
Copyright (c) 2015,xuetangx
All rights reserved.

摘    要: download.py 从youtube下载视频到本地
创 建 者: ZuoBin
创建日期: 2015-05-12
'''

import os
import subprocess
import time
import logging
import datetime

from model import CourseRss, Course
from settings import PROXY_SERVER, YOUTUBE_PATH
from upload import upload_videos 
from lib.database import trans

PATH = os.path.dirname(os.path.abspath(__file__))

def wait_process_end(process, timeout):
    '''等待进程终止
    Args:
        process: 进程句柄
        timeout: 超时时间
    Returns:
        与shell的执行保持一致
        0:成功
        1:超时
        2:错误
    '''
    if timeout <= 0:
        process.wait()
        return 0
    start_time = time.time()
    end_time = start_time + timeout
    while 1:
        ret = process.poll()
        if ret == 0:
            return 0
        elif ret is None:
            cur_time = time.time()
            if cur_time >= end_time:
                return 1
            time.sleep(0.1)
        else:
            return 2


class ShellResult(object):

    '''封装shell执行的返回结果形式
    Attributes:
        return_code: 返回码
        stdout：标准输出
        stderr: 错误输出
    '''

    def __init__(self, return_code, stdout, stderr):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr


def shell(command, timeout=0, capture=False, debug=False):
    '''用于执行本地shell的功能
    Args:
        command: bash命令
        timeout: 命令的超时时间
        capture: 是否捕获输出结果
        debug: 是否输出debug信息
    Returns:
        返回ShellResult对象
    '''
    if debug:
        print '=' * 35
        print '[local] ' + command
        print '=' * 35
    if capture:
        process = subprocess.Popen(command, stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   shell=True)
    else:
        process = subprocess.Popen(command, shell=True)
    ret = wait_process_end(process, timeout)
    if ret == 1:
        process.terminate()
        raise Exception("terminated_for_timout")
    if capture:
        stdout = ''.join(process.stdout.readlines())
        stderr = ''.join(process.stderr.readlines())
        return ShellResult(process.returncode, stdout, stderr)
    else:
        return ShellResult(process.returncode, None, None)

def get_course():
    '''获得需要下载的课程视频信息
    '''
    course_list = CourseRss.mgr().Q()
    need_download_list = []
    for course in course_list:
        if course.video_url and not course.ccid:
            need_download_list.append(course)
    return need_download_list

def download_video(course_rss):
    '''下载视频
    Args:
        course_rss: rss课程信息
    Returns:
        video的文件名
    '''
    try:
        # 获取文件名
        base_order = YOUTUBE_PATH + " {0} --proxy {1} {2}"
        video_id_order = base_order.format('--get-id', PROXY_SERVER, course_rss.video_url) 
        video_ret = shell(video_id_order, capture=True, debug=False)
        video_id = video_ret.stdout.strip()
        # 进入指定的文件夹并下载课程视频
        enter_order = "cd %s/download/" % PATH
        download_order = base_order.format('--id', PROXY_SERVER, course_rss.video_url)
        fin_order = '{0} ; {1}'.format(enter_order, download_order)
        download_ret = shell(fin_order, capture=True, debug=False)
        # 异常情况
        if download_ret.stderr:
            logging.error('download error, error is %s'% download_ret.stderr, exc_info=True)
            return ''
        return video_id
    except Exception, e:
        logging.error('Error is %s'% e, exc_info=True)
    return ''

def upload_single_video(file_addr):
    '''上传视频文件至cc
    Args:
        file_addr: 文件绝对路径
    Returns:
       ccid
    '''
    ccid = ''
    if os.path.exists(file_addr):
        ccid = upload_videos(file_addr)
    return ccid

def get_file_addr(video_id):
    '''根据视频文件的id来查找视频文件绝对路径
    Args:
        video_id: 视频文件的id
    Returns:
        文件绝对路径
    '''
    file_path = ''
    if video_id:
        dir_list = os.listdir(PATH + '/download/')
        for ff in dir_list:
            if video_id in ff:
                file_path = PATH + '/download/%s' % ff
    return file_path

@trans(CourseRss)
def update_course_rss(course_id, video_id, ccid):
    '''更新rss课程信息，并且更新xuetang课程的ccid
    Args:
        course_id: 课程id
        video_id: 下载视频的文件id
        ccid: cc唯一标示
    '''
    cr = CourseRss.mgr(ismaster=True).Q().filter(course_id=course_id)[0]
    if cr:
        cr.ccid = ccid
        cr.video_id = video_id
        cr.upload_time = datetime.datetime.now()
        cr.update()

    cou = Course.mgr(ismaster=True).Q().filter(course_id=course_id)[0]
    if cou:
        cou.intro_video = ccid
        cou.update()
        
def delete_file(file_path):
    '''上传cc后删除本地视频文件，以免占用服务器存储
    '''
    if os.path.exists(file_path):
        os.remove(file_path) 
        
def main():
    '''主方法函数,整个下载并上传cc的流程
    '''
    # 获取课程下载信息
    course_list = get_course()
    for course in course_list:
        # 下载视频
        video_id = download_video(course)
        # 获得文件绝对路径
        file_path = get_file_addr(video_id)
        # 上传到cc
        ccid = upload_single_video(file_path)
        # 修改数据库
        if ccid:
            update_course_rss(course.course_id, video_id, ccid)
            # 删除视频文件
            delete_file(file_path) 

if __name__ == '__main__':
    pre_order = "cd /edx/app/edxapp/edx-platform/rss/download"
    download_order = "youtube-dl --id  --proxy 192.168.100.35:808 'https://www.youtube.com/watch?v=dbpXgfXJWNQ'"
    order = '%s ; %s' % (pre_order, download_order)
    ret = shell(order, capture=True, debug=True)
    print ret.stdout
    print ret.stderr

    
