# coding=utf-8

import os
from ctypes import *

from HCNetSDK import sys_platform, system_type, C_DWORD

if sys_platform == 'linux':
    load_library = cdll.LoadLibrary
    fun_ctype = CFUNCTYPE
elif sys_platform == 'windows':
    load_library = windll.LoadLibrary
    fun_ctype = WINFUNCTYPE
else:
    print("************不支持的平台**************")
    exit(0)

playM4dllpath_dict = {'windows64': os.path.dirname(__file__) + '\\lib\\' + 'PlayCtrl.dll',
                      'windows32': os.path.dirname(__file__) + '\\lib\\' + 'PlayCtrl.dll',
                      'linux64': os.path.dirname(__file__) + '/lib/libPlayCtrl.so',
                      'linux32': os.path.dirname(__file__) + '/lib/libPlayCtrl.so'}
playM4dllpath = playM4dllpath_dict[system_type]


# 定义预览参数结构体
class FRAME_INFO(Structure):
    _fields_ = [
        ('nWidth', c_long),
        ('nHeight', c_long),
        ('nStamp', c_long),
        ('nType', c_long),
        ('nFrameRate', c_long),
        ('dwFrameNum', C_DWORD)
    ]


LPFRAME_INFO = POINTER(FRAME_INFO)

# 显示回调函数
DISPLAYCBFUN = fun_ctype(None, c_long, c_char_p, c_long, c_long, c_long, c_long, c_long, c_long)
# 解码回调函数
DECCBFUNWIN = fun_ctype(None, c_long, POINTER(c_char), c_long, POINTER(FRAME_INFO), c_long, c_long)
