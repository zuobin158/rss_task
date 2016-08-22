# -*- coding: utf-8 -*-

import sys
import os
import re
import logging

from settings import UPLOAD_JAR_PATH, JAVA_PATH


def upload_videos(in_path): 
    if os.path.isfile(in_path):
        return upload2cc(in_path)
    return None

def upload2cc(video_path):
    '''上传视频到cc
    Args:
        video_path: 视频文件路径
    '''
    upload_cmd_str = JAVA_PATH + " -jar %s %s 'None'" % (UPLOAD_JAR_PATH, video_path)
    try:
        upload_log = os.popen(r"%s" % upload_cmd_str).read()
        vid_info = re.findall(r'VID:\w+\s+video path:.+', upload_log)
        infoDict = getccid_by_uploadinfo(vid_info[0])
        ccid = infoDict.get('ccid', "")
        if ccid == "":
            logging.error("Error: %s" % infoDict.get('error', ""))
    except Exception, e:
        ccid = ""
        logging.error("Error is %s, video_path is %s" % (e, video_path), exc_info=True)
    return ccid

def getccid_by_uploadinfo(vid_info):
    '''获取ccid
    Args:
        vid_info: 下载的日志信息，包含ccid
    Returns:
       ccid
    '''
    res = {}
    ccid_index_start = vid_info.find("VID:") + 4
    ccid_index_end = vid_info.find("\t")
    if ccid_index_start == -1 or ccid_index_end == -1:
        res['error'] = vid_info
        return res
    ccid = vid_info[ccid_index_start:ccid_index_end]
    res['ccid'] = ccid
    return res

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, '1.mp4')
    ccid = upload_videos(path)
