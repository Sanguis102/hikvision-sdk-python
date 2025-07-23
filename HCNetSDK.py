# -*- coding: utf-8 -*-
# @Time : 2024/8/6 16:31
# @Author : sdk007

import os
import platform
import re
from ctypes import *
from enum import Enum


def system_get_platform_info():
    sys_platform = platform.system().lower().strip()
    python_bit = platform.architecture()[0]
    python_bit_num = re.findall('(\d+)\w*', python_bit)[0]
    return sys_platform, python_bit_num


sys_platform, python_bit_num = system_get_platform_info()
system_type = sys_platform + python_bit_num

if sys_platform == 'linux':
    load_library = cdll.LoadLibrary
    fun_ctype = CFUNCTYPE
elif sys_platform == 'windows':
    load_library = windll.LoadLibrary
    fun_ctype = WINFUNCTYPE
else:
    print("************不支持的平台**************")
    exit(0)

netsdkdllpath_dict = {'windows64': os.path.dirname(__file__) + '\\lib\\' + 'HCNetSDK.dll',
                      'windows32': os.path.dirname(__file__) + '\\lib\\' + 'HCNetSDK.dll',
                      'linux64': os.path.dirname(__file__) + '/lib/libhcnetsdk.so',
                      'linux32': os.path.dirname(__file__) + '/lib/libhcnetsdk.so'}
netsdkdllpath = netsdkdllpath_dict[system_type]

C_LLONG_DICT = {'windows64': c_longlong, 'windows32': c_long, 'linux32': c_long, 'linux64': c_long}
C_LONG_DICT = {'windows64': c_long, 'windows32': c_long, 'linux32': c_int, 'linux64': c_int}
C_LDWORD_DICT = {'windows64': c_longlong, 'windows32': c_ulong, 'linux32': c_long, 'linux64': c_long}
C_DWORD_DICT = {'windows64': c_ulong, 'windows32': c_ulong, 'linux32': c_uint, 'linux64': c_uint}
C_HWND_DICT = {'windows64': c_void_p, 'windows32': c_void_p, 'linux32': c_uint, 'linux64': c_uint}

C_LLONG = C_LLONG_DICT[system_type]
C_LONG = C_LONG_DICT[system_type]
C_LDWORD = C_LDWORD_DICT[system_type]
C_DWORD = C_DWORD_DICT[system_type]
# C_BOOL = c_int
# C_UINT = c_uint
# C_BYTE = c_ubyte
# C_ENUM = c_int

C_HWND = C_HWND_DICT[system_type]
C_WORD = c_ushort
C_USHORT = c_ushort
C_SHORT = c_short
# C_LONG = c_int
C_BYTE = c_ubyte
C_UINT = c_uint
C_LPVOID = c_void_p
C_HANDLE = c_void_p
C_LPDWORD = POINTER(c_uint)
C_UINT64 = c_ulonglong
C_INT64 = c_longlong
C_BOOL = c_int

NET_DVR_GET_NETCFG = 102  # 获取网络参数
NET_DVR_GET_NETCFG_V50 = 1015  # 获取网络参数
NET_DVR_SET_NETCFG_V50 = 1016  # 设置网络参数

# 码流回调数据类型
NET_DVR_SYSHEAD = 1
NET_DVR_STREAMDATA = 2
NET_DVR_AUDIOSTREAMDATA = 3
NET_DVR_PRIVATE_DATA = 112


# 枚举定义
# SDK本地参数类型枚举
class NET_SDK_LOCAL_CFG_TYPE(Enum):
    NET_SDK_LOCAL_CFG_TYPE_TCP_PORT_BIND = 0  # 本地TCP端口绑定配置，对应结构体NET_DVR_LOCAL_TCP_PORT_BIND_CFG
    NET_SDK_LOCAL_CFG_TYPE_UDP_PORT_BIND = 1  # 本地UDP端口绑定配置，对应结构体NET_DVR_LOCAL_UDP_PORT_BIND_CFG
    NET_SDK_LOCAL_CFG_TYPE_MEM_POOL = 2  # 内存池本地配置，对应结构体NET_DVR_LOCAL_MEM_POOL_CFG
    NET_SDK_LOCAL_CFG_TYPE_MODULE_RECV_TIMEOUT = 3  # 按模块配置超时时间，对应结构体NET_DVR_LOCAL_MODULE_RECV_TIMEOUT_CFG
    NET_SDK_LOCAL_CFG_TYPE_ABILITY_PARSE = 4  # 是否使用能力集解析库，对应结构体NET_DVR_LOCAL_ABILITY_PARSE_CFG
    NET_SDK_LOCAL_CFG_TYPE_TALK_MODE = 5  # 对讲模式，对应结构体NET_DVR_LOCAL_TALK_MODE_CFG
    NET_SDK_LOCAL_CFG_TYPE_PROTECT_KEY = 6  # 密钥设置，对应结构体NET_DVR_LOCAL_PROTECT_KEY_CFG
    NET_SDK_LOCAL_CFG_TYPE_CFG_VERSION = 7  # 用于测试版本头的设备端兼容情NET_DVR_LOCAL_MEM_POOL_CFG况, 只有在设置参数时才起作用。
    NET_SDK_LOCAL_CFG_TYPE_RTSP_PARAMS = 8  # rtsp参数配置，对于结构体NET_DVR_RTSP_PARAMS_CFG
    NET_SDK_LOCAL_CFG_TYPE_SIMXML_LOGIN = 9  # 在登录时使用模拟能力补充support字段, 对应结构NET_DVR_SIMXML_LOGIN
    NET_SDK_LOCAL_CFG_TYPE_CHECK_DEV = 10  # 心跳交互间隔时间
    NET_SDK_LOCAL_CFG_TYPE_SECURITY = 11  # SDK本次安全配置，
    NET_SDK_LOCAL_CFG_TYPE_EZVIZLIB_PATH = 12  # 配置萤石云通信库地址，
    NET_SDK_LOCAL_CFG_TYPE_CHAR_ENCODE = 13  # 13.配置字符编码相关处理回调
    NET_SDK_LOCAL_CFG_TYPE_PROXYS = 14  # 设置获取代
    NET_DVR_LOCAL_CFG_TYPE_LOG = 15  # 日志参数配置  NET_DVR_LOCAL_LOG_CFG
    NET_DVR_LOCAL_CFG_TYPE_STREAM_CALLBACK = 16  # 码流回调参数配置 NET_DVR_LOCAL_STREAM_CALLBACK_CFG
    NET_DVR_LOCAL_CFG_TYPE_GENERAL = 17  # 通用参数配置 NET_DVR_LOCAL_GENERAL_CFG
    NET_DVR_LOCAL_CFG_TYPE_PTZ = 17  # PTZ是否接收设备返回配置
    NET_DVR_LOCAL_CFG_MESSAGE_CALLBACK_V51 = 19  # 报警V51回调相关本地配置,对应结构体为NET_DVR_MESSAGE_CALLBACK_PARAM_V51 。(仅对NET_DVR_SetDVRMessageCallBack_V51以上版本有效)
    NET_SDK_LOCAL_CFG_CERTIFICATION = 20  # 配置和证书相关的参数，对应结构体结构体NET_DVR_LOCAL_CERTIFICATION
    NET_SDK_LOCAL_CFG_PORT_MULTIPLEX = 21  # 端口复用，对应结构体NET_DVR_LOCAL_PORT_MULTI_CFG
    NET_SDK_LOCAL_CFG_ASYNC = 22  # 异步配置，对应结构体NET_DVR_LOCAL_ASYNC_CFG
    NET_SDK_P2P_LOGIN_2C = 23
    NET_SDK_P2P_LOGIN_2B = 24
    NET_SDK_P2P_LOGOUT = 25
    NET_SDK_AUDIOCAST_CFG = 26  # 配置广播采样率 ,对应结构体NET_LOCAL_AUDIOCAST_CFG


# 设置SDK初始化参数类型枚举
class NET_SDK_INIT_CFG_TYPE(Enum):
    NET_SDK_INIT_CFG_TYPE_CHECK_MODULE_COM = 0  # 增加对必须库的检查
    NET_SDK_INIT_CFG_ABILITY = 1  # sdk支持的业务的能力集
    NET_SDK_INIT_CFG_SDK_PATH = 2  # 设置HCNetSDK库所在目录
    NET_SDK_INIT_CFG_LIBEAY_PATH = 3  # 设置OpenSSL的libeay32.dll/libcrypto.so/libcrypto.dylib所在路径
    NET_SDK_INIT_CFG_SSLEAY_PATH = 4  # 设置OpenSSL的ssleay32.dll/libssl.so/libssl.dylib所在路径


# 事件类型枚举
class ALARM_LCOMMAND_ENUM(Enum):
    COMM_ALARM_ACS = 0x5002  # 门禁主机报警信息,对应数据类型结构体：NET_DVR_ACS_ALARM_INFO
    COMM_ID_INFO_ALARM = 0x5200  # 门禁身份证刷卡信息,对应数据类型结构体：NET_DVR_ID_CARD_INFO_ALARM
    COMM_ALARM_V30 = 0x4000  # 移动侦测、视频丢失、遮挡、IO信号量等报警信息(V3.0以上版本支持的设备),对应数据类型结构体：NET_DVR_ALARMINFO_V30
    COMM_ISAPI_ALARM = 0x6009  # 智能检测报警(封装结构体，图片数据分离),对应数据类型结构体：NET_DVR_ALARM_ISAPI_INFO
    COMM_UPLOAD_FACESNAP_RESULT = 0x1112  # 人脸抓拍结果信息,对应数据类型结构体：NET_VCA_FACESNAP_RESULT
    COMM_SNAP_MATCH_ALARM = 0x2902  # 人脸比对结果信息,对应数据类型结构体：NET_VCA_FACESNAP_MATCH_ALARM


# 设备参数结构体 V30
class NET_DVR_DEVICEINFO_V30(Structure):
    _fields_ = [
        ("sSerialNumber", C_BYTE * 48),  # 序列号
        ("byAlarmInPortNum", C_BYTE),  # 模拟报警输入个数
        ("byAlarmOutPortNum", C_BYTE),  # 模拟报警输出个数
        ("byDiskNum", C_BYTE),  # 硬盘个数
        ("byDVRType", C_BYTE),  # 设备类型
        ("byChanNum", C_BYTE),  # 设备模拟通道个数，数字（IP）通道最大个数为byIPChanNum + byHighDChanNum*256
        ("byStartChan", C_BYTE),  # 模拟通道的起始通道号，从1开始。数字通道的起始通道号见下面参数byStartDChan
        ("byAudioChanNum", C_BYTE),  # 设备语音对讲通道数
        ("byIPChanNum", C_BYTE),  # 设备最大数字通道个数，低8位，高8位见byHighDChanNum
        ("byZeroChanNum", C_BYTE),  # 零通道编码个数
        ("byMainProto", C_BYTE),  # 主码流传输协议类型：0- private，1- rtsp，2- 同时支持私有协议和rtsp协议取流（默认采用私有协议取流）
        ("bySubProto", C_BYTE),  # 子码流传输协议类型：0- private，1- rtsp，2- 同时支持私有协议和rtsp协议取流（默认采用私有协议取流）
        ("bySupport", C_BYTE),  # 能力，位与结果为0表示不支持，1表示支持
        # bySupport & 0x1，表示是否支持智能搜索
        # bySupport & 0x2，表示是否支持备份
        # bySupport & 0x4，表示是否支持压缩参数能力获取
        # bySupport & 0x8, 表示是否支持双网卡
        # bySupport & 0x10, 表示支持远程SADP
        # bySupport & 0x20, 表示支持Raid卡功能
        # bySupport & 0x40, 表示支持IPSAN目录查找
        # bySupport & 0x80, 表示支持rtp over rtsp
        ("bySupport1", C_BYTE),  # 能力集扩充，位与结果为0表示不支持，1表示支持
        # bySupport1 & 0x1, 表示是否支持snmp v30
        # bySupport1 & 0x2, 表示是否支持区分回放和下载
        # bySupport1 & 0x4, 表示是否支持布防优先级
        # bySupport1 & 0x8, 表示智能设备是否支持布防时间段扩展
        # bySupport1 & 0x10,表示是否支持多磁盘数（超过33个）
        # bySupport1 & 0x20,表示是否支持rtsp over http
        # bySupport1 & 0x80,表示是否支持车牌新报警信息，且还表示是否支持NET_DVR_IPPARACFG_V40配置
        ("bySupport2", C_BYTE),  # 能力集扩充，位与结果为0表示不支持，1表示支持
        # bySupport2 & 0x1, 表示解码器是否支持通过URL取流解码
        # bySupport2 & 0x2, 表示是否支持FTPV40
        # bySupport2 & 0x4, 表示是否支持ANR(断网录像)
        # bySupport2 & 0x20, 表示是否支持单独获取设备状态子项
        # bySupport2 & 0x40, 表示是否是码流加密设备
        ("wDevType", C_WORD),  # 设备型号，详见下文列表
        ("bySupport3", C_BYTE),  # 能力集扩展，位与结果：0- 不支持，1- 支持
        # bySupport3 & 0x1, 表示是否支持多码流
        # bySupport3 & 0x4, 表示是否支持按组配置，具体包含通道图像参数、报警输入参数、IP报警输入/输出接入参数、用户参数、设备工作状态、JPEG抓图、定时和时间抓图、硬盘盘组管理等
        # bySupport3 & 0x20, 表示是否支持通过DDNS域名解析取流
        ("byMultiStreamProto", C_BYTE),  # 是否支持多码流，按位表示，位与结果：0-不支持，1-支持
        # byMultiStreamProto & 0x1, 表示是否支持码流3
        # byMultiStreamProto & 0x2, 表示是否支持码流4
        # byMultiStreamProto & 0x40,表示是否支持主码流
        # byMultiStreamProto & 0x80,表示是否支持子码流
        ("byStartDChan", C_BYTE),  # 起始数字通道号，0表示无数字通道，比如DVR或IPC
        ("byStartDTalkChan", C_BYTE),  # 起始数字对讲通道号，区别于模拟对讲通道号，0表示无数字对讲通道
        ("byHighDChanNum", C_BYTE),  # 数字通道个数，高8位
        ("bySupport4", C_BYTE),  # 能力集扩展，按位表示，位与结果：0- 不支持，1- 支持
        # bySupport4 & 0x01, 表示是否所有码流类型同时支持RTSP和私有协议
        # bySupport4 & 0x10, 表示是否支持域名方式挂载网络硬盘
        ("byLanguageType", C_BYTE),  # 支持语种能力，按位表示，位与结果：0- 不支持，1- 支持
        # byLanguageType ==0，表示老设备，不支持该字段
        # byLanguageType & 0x1，表示是否支持中文
        # byLanguageType & 0x2，表示是否支持英文
        ("byVoiceInChanNum", C_BYTE),  # 音频输入通道数
        ("byStartVoiceInChanNo", C_BYTE),  # 音频输入起始通道号，0表示无效
        ("bySupport5", C_BYTE),  # 按位表示,0-不支持,1-支持,bit0-支持多码流
        ("bySupport6", C_BYTE),  # 按位表示,0-不支持,1-支持
        # bySupport6 & 0x1  表示设备是否支持压缩
        # bySupport6 & 0x2  表示是否支持流ID方式配置流来源扩展命令，DVR_SET_STREAM_SRC_INFO_V40
        # bySupport6 & 0x4  表示是否支持事件搜索V40接口
        # bySupport6 & 0x8  表示是否支持扩展智能侦测配置命令
        # bySupport6 & 0x40 表示图片查询结果V40扩展
        ("byMirrorChanNum", C_BYTE),  # 镜像通道个数，录播主机中用于表示导播通道
        ("wStartMirrorChanNo", C_WORD),  # 起始镜像通道号
        ("bySupport7", C_BYTE),  # 能力,按位表示,0-不支持,1-支持
        # bySupport7 & 0x1  表示设备是否支持NET_VCA_RULECFG_V42扩展
        # bySupport7 & 0x2  表示设备是否支持IPC HVT 模式扩展
        # bySupport7 & 0x04 表示设备是否支持返回锁定时间
        # bySupport7 & 0x08 表示设置云台PTZ位置时，是否支持带通道号
        # bySupport7 & 0x10 表示设备是否支持双系统升级备份
        # bySupport7 & 0x20 表示设备是否支持OSD字符叠加V50
        # bySupport7 & 0x40 表示设备是否支持主从（从摄像机）
        # bySupport7 & 0x80 表示设备是否支持报文加密
        ("byRes2", C_BYTE)]  # 保留，置为0


LPNET_DVR_DEVICEINFO_V30 = POINTER(NET_DVR_DEVICEINFO_V30)


# 设备参数结构体 V40
class NET_DVR_DEVICEINFO_V40(Structure):
    _fields_ = [
        ('struDeviceV30', NET_DVR_DEVICEINFO_V30),  # 设备信息
        ('bySupportLock', C_BYTE),  # 设备支持锁定功能，该字段由SDK根据设备返回值来赋值的。bySupportLock为1时，dwSurplusLockTime和byRetryLoginTime有效
        ('byRetryLoginTime', C_BYTE),  # 剩余可尝试登陆的次数，用户名，密码错误时，此参数有效
        ('byPasswordLevel', C_BYTE),  # admin密码安全等级
        ('byProxyType', C_BYTE),  # 代理类型，0-不使用代理, 1-使用socks5代理, 2-使用EHome代理
        ('dwSurplusLockTime', C_DWORD),  # 剩余时间，单位秒，用户锁定时，此参数有效
        ('byCharEncodeType', C_BYTE),  # 字符编码类型
        ('bySupportDev5', C_BYTE),  # 支持v50版本的设备参数获取，设备名称和设备类型名称长度扩展为64字节
        ('bySupport', C_BYTE),  # 能力集扩展，位与结果：0- 不支持，1- 支持
        ('byLoginMode', C_BYTE),  # 登录模式:0- Private登录，1- ISAPI登录
        ('dwOEMCode', C_DWORD),  # OEM Code
        ('iResidualValidity', C_LONG),  # 该用户密码剩余有效天数，单位：天，返回负值，表示密码已经超期使用，例如“-3表示密码已经超期使用3天”
        ('byResidualValidity', C_BYTE),  # iResidualValidity字段是否有效，0-无效，1-有效
        ('bySingleStartDTalkChan', C_BYTE),  # 独立音轨接入的设备，起始接入通道号，0-为保留字节，无实际含义，音轨通道号不能从0开始
        ('bySingleDTalkChanNums', C_BYTE),  # 独立音轨接入的设备的通道总数，0-表示不支持
        ('byPassWordResetLevel', C_BYTE),  # 0-无效，
        # 1- 管理员创建一个非管理员用户为其设置密码，该非管理员用户正确登录设备后要提示“请修改初始登录密码”，未修改的情况下，用户每次登入都会进行提醒；
        # 2- 当非管理员用户的密码被管理员修改，该非管理员用户再次正确登录设备后，需要提示“请重新设置登录密码”，未修改的情况下，用户每次登入都会进行提醒。
        ('bySupportStreamEncrypt', C_BYTE),  # 能力集扩展，位与结果：0- 不支持，1- 支持
        # bySupportStreamEncrypt & 0x1 表示是否支持RTP/TLS取流
        # bySupportStreamEncrypt & 0x2 表示是否支持SRTP/UDP取流
        # bySupportStreamEncrypt & 0x4 表示是否支持SRTP/MULTICAST取流
        ('byMarketType', C_BYTE),  # 0-无效（未知类型）,1-经销型，2-行业型
        ('byRes2', C_BYTE * 238)  # 保留，置为0
    ]


LPNET_DVR_DEVICEINFO_V40 = POINTER(NET_DVR_DEVICEINFO_V40)

# 异步登录回调函数
fLoginResultCallBack = fun_ctype(None, C_LONG, C_DWORD, LPNET_DVR_DEVICEINFO_V30, c_void_p)


# NET_DVR_Login_V40()参数
class NET_DVR_USER_LOGIN_INFO(Structure):
    _fields_ = [
        ("sDeviceAddress", c_char * 129),  # 设备地址，IP 或者普通域名
        ("byUseTransport", C_BYTE),  # 是否启用能力集透传：0- 不启用透传，默认；1- 启用透传
        ("wPort", C_WORD),  # 设备端口号，例如：8000
        ("sUserName", c_char * 64),  # 登录用户名，例如：admin
        ("sPassword", c_char * 64),  # 登录密码，例如：12345
        ("cbLoginResult", fLoginResultCallBack),  # 登录状态回调函数，bUseAsynLogin 为1时有效
        ("pUser", C_LPVOID),  # 用户数据
        ("bUseAsynLogin", C_DWORD),  # 是否异步登录：0- 否，1- 是
        ("byProxyType", C_BYTE),  # 0:不使用代理，1：使用标准代理，2：使用EHome代理
        ("byUseUTCTime", C_BYTE),
        # 0-不进行转换，默认,1-接口上输入输出全部使用UTC时间,SDK完成UTC时间与设备时区的转换,2-接口上输入输出全部使用平台本地时间，SDK完成平台本地时间与设备时区的转换
        ("byLoginMode", C_BYTE),  # 0-Private 1-ISAPI 2-自适应
        ("byHttps", C_BYTE),  # 0-不适用tls，1-使用tls 2-自适应
        ("iProxyID", C_DWORD),  # 代理服务器序号，添加代理服务器信息时，相对应的服务器数组下表值
        ("byVerifyMode", C_BYTE),  # 认证方式，0-不认证，1-双向认证，2-单向认证；认证仅在使用TLS的时候生效;
        ("byRes2", C_BYTE * 119)]


LPNET_DVR_USER_LOGIN_INFO = POINTER(NET_DVR_USER_LOGIN_INFO)


# 组件库加载路径信息
class NET_DVR_LOCAL_SDK_PATH(Structure):
    _fields_ = [
        ('sPath', c_char * 256),  # 组件库地址
        ('byRes', C_BYTE * 128),
    ]


LPNET_DVR_LOCAL_SDK_PATH = POINTER(NET_DVR_LOCAL_SDK_PATH)


# 报警设备信息结构体
class NET_DVR_ALARMER(Structure):
    _fields_ = [
        ("byUserIDValid", C_BYTE),  # UserID是否有效 0-无效，1-有效
        ("bySerialValid", C_BYTE),  # 序列号是否有效 0-无效，1-有效
        ("byVersionValid", C_BYTE),  # 版本号是否有效 0-无效，1-有效
        ("byDeviceNameValid", C_BYTE),  # 设备名字是否有效 0-无效，1-有效
        ("byMacAddrValid", C_BYTE),  # MAC地址是否有效 0-无效，1-有效
        ("byLinkPortValid", C_BYTE),  # login端口是否有效 0-无效，1-有效
        ("byDeviceIPValid", C_BYTE),  # 设备IP是否有效 0-无效，1-有效
        ("bySocketIPValid", C_BYTE),  # socket ip是否有效 0-无效，1-有效
        ("lUserID", C_LONG),  # NET_DVR_Login()返回值, 布防时有效
        ("sSerialNumber", C_BYTE * 48),  # 序列号
        ("dwDeviceVersion", C_DWORD),  # 版本信息 高16位表示主版本，低16位表示次版本
        ("sDeviceName", C_BYTE * 32),  # 设备名字
        ("byMacAddr", C_BYTE * 6),  # MAC地址
        ("wLinkPort", C_WORD),  # link port
        ("sDeviceIP", C_BYTE * 128),  # IP地址
        ("sSocketIP", C_BYTE * 128),  # 报警主动上传时的socket IP地址
        ("byIpProtocol", C_BYTE),  # Ip协议 0-IPV4, 1-IPV6
        ("byRes2", C_BYTE * 11)]


LPNET_DVR_ALARMER = POINTER(NET_DVR_ALARMER)


# 报警布防参数结构体
class NET_DVR_SETUPALARM_PARAM(Structure):
    _fields_ = [
        ("dwSize", C_DWORD),  # 结构体大小
        ("byLevel", C_BYTE),  # 布防优先级：0- 一等级（高），1- 二等级（中），2- 三等级（低）
        ("byAlarmInfoType", C_BYTE),
        # 上传报警信息类型（抓拍机支持），0-老报警信息（NET_DVR_PLATE_RESULT），1-新报警信息(NET_ITS_PLATE_RESULT)2012-9-28
        ("byRetAlarmTypeV40", C_BYTE),
        # 0- 返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO,
        # 1- 设备支持NET_DVR_ALARMINFO_V40则返回NET_DVR_ALARMINFO_V40，不支持则返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO
        ("byRetDevInfoVersion", C_BYTE),  # CVR上传报警信息回调结构体版本号 0-COMM_ALARM_DEVICE， 1-COMM_ALARM_DEVICE_V40
        ("byRetVQDAlarmType", C_BYTE),  # VQD报警上传类型，0-上传报报警NET_DVR_VQD_DIAGNOSE_INFO，1-上传报警NET_DVR_VQD_ALARM
        ("byFaceAlarmDetection", C_BYTE),
        ("bySupport", C_BYTE),
        ("byBrokenNetHttp", C_BYTE),
        ("wTaskNo", C_WORD),
        # 任务处理号 和 (上传数据NET_DVR_VEHICLE_RECOG_RESULT中的字段dwTaskNo对应 同时 下发任务结构 NET_DVR_VEHICLE_RECOG_COND中的字段dwTaskNo对应)
        ("byDeployType", C_BYTE),  # 布防类型：0-客户端布防，1-实时布防
        ("byRes1", C_BYTE * 3),
        ("byAlarmTypeURL", C_BYTE),
        # bit0-表示人脸抓拍报警上传
        # 0-表示二进制传输，1-表示URL传输（设备支持的情况下，设备支持能力根据具体报警能力集判断,同时设备需要支持URL的相关服务，当前是”云存储“）
        ("byCustomCtrl", C_BYTE)]  # Bit0- 表示支持副驾驶人脸子图上传: 0-不上传,1-上传


LPNET_DVR_SETUPALARM_PARAM = POINTER(NET_DVR_SETUPALARM_PARAM)


# 上传的报警信息结构体。
class NET_DVR_ALARMINFO_V30(Structure):
    _fields_ = [
        ("dwAlarmType", c_uint32),  # 报警类型
        ("dwAlarmInputNumber", c_uint32),  # 报警输入端口，当报警类型为0、23时有效
        ("byAlarmOutputNumber", c_byte * 96),
        # 触发的报警输出端口，值为1表示该报警端口输出，如byAlarmOutputNumber[0]=1表示触发第1个报警输出口输出，byAlarmOutputNumber[1]=1表示触发第2个报警输出口，依次类推
        ("byAlarmRelateChannel", c_byte * 64),  # 触发的录像通道，值为1表示该通道录像，如byAlarmRelateChannel[0]=1表示触发第1个通道录像
        ("byChannel", c_byte * 64),  # 发生报警的通道。当报警类型为2、3、6、9、10、11、13、15、16时有效，如byChannel[0]=1表示第1个通道报警
        ("byDiskNumber", c_byte * 33)]  # 发生报警的硬盘。当报警类型为1，4，5时有效，byDiskNumber[0]=1表示1号硬盘异常


LPNET_DVR_ALARMINFO_V30 = POINTER(NET_DVR_ALARMINFO_V30)


# 时间参数结构体
class NET_DVR_TIME_EX(Structure):
    _fields_ = [
        ("dwYear", c_ushort),
        ("dwMonth", c_ubyte),
        ("dwDay", c_ubyte),
        ("dwHour", c_ubyte),
        ("dwMinute", c_ubyte),
        ("dwSecond", c_ubyte),
        ("byRes", c_ubyte)
    ]


LPNET_DVR_TIME_EX = POINTER(NET_DVR_TIME_EX)


# 防区参数结构体。
class NET_DVR_ALARMIN_SETUP(Structure):
    _fields_ = [
        ("byAssiciateAlarmIn", C_BYTE * 512),  # 报警类型
        ("byRes", C_BYTE * 100)
    ]


LPNET_DVR_ALARMIN_SETUP = POINTER(NET_DVR_ALARMIN_SETUP)


# CID报警信息结构体。
class NET_DVR_CID_ALARM(Structure):
    _fields_ = [
        ("dwAlarmType", C_DWORD),  # 报警类型
        ("sCIDCode", C_BYTE * 4),  # CID事件号，参照NET_DVR_ALARMHOST_CID_ALL_MINOR_TYPE
        ("sCIDDescribe", C_BYTE * 32),  # CID事件名
        ("struTriggerTime", NET_DVR_TIME_EX),  # 触发报警的时间点
        ("struUploadTime", NET_DVR_TIME_EX),  # 上传报警的时间点
        ("sCenterAccount", C_BYTE * 6),  # 中心帐号，byCenterType为0或1时有效
        ("byReportType", C_BYTE),  # 报告类型，具体定义参考NET_DVR_ALARMHOST_REPORT_TYPE
        ("byUserType", C_BYTE),  # 用户类型：0-网络用户，1-键盘用户
        ("sUserName", C_BYTE * 32),  # 网络用户用户名
        ("wKeyUserNo", C_WORD),  # 键盘用户号，0xFFFF表示无效
        ("byKeypadNo", C_BYTE),  # 键盘号，0xFF表示无效
        ("bySubSysNo", C_BYTE),  # 子系统号，0xFF表示无效
        ("wDefenceNo", C_WORD),  # 防区号，0xFFFF表示无效
        ("byVideoChanNo", C_BYTE),  # 视频通道号，0xFF表示无效
        ("byDiskNo", C_BYTE),  # 硬盘号，0xFF表示无效
        ("wModuleAddr", C_WORD),  # 模块地址，0xFFFF表示无效
        ("byCenterType", C_BYTE),  # 中心账号类型：0- 无效，1- 中心账号(长度6)，2- 扩展的中心账号(长度32)
        ("byRes1", C_BYTE),  # 保留
        ("sCenterAccountV40", C_BYTE * 32),  # 中心账号扩展，byCenterType为2时有效
        ("byRes2", C_BYTE * 28)  # 保留
    ]


LPNET_DVR_CID_ALARM = POINTER(NET_DVR_CID_ALARM)


# 时间参数结构体
class NET_DVR_TIME(Structure):
    _fields_ = [
        ("dwYear", C_DWORD),  # 年
        ("dwMonth", C_DWORD),  # 月
        ("dwDay", C_DWORD),  # 日
        ("dwHour", C_DWORD),  # 时
        ("dwMinute", C_DWORD),  # 分
        ("dwSecond", C_DWORD)]  # 秒


LPNET_DVR_TIME = POINTER(NET_DVR_TIME)


# IP地址结构体
class NET_DVR_IPADDR(Structure):
    _fields_ = [
        ("sIpV4", c_char * 16),  # 设备IPv4地址
        ("sIpV6", C_BYTE * 128)]  # 设备IPv6地址


LPNET_DVR_IPADDR = POINTER(NET_DVR_IPADDR)


# 门禁主机事件信息
class NET_DVR_ACS_EVENT_INFO(Structure):
    _fields_ = [
        ("dwSize", C_DWORD),  # 结构体大小
        ("byCardNo", C_BYTE * 32),  # 卡号
        ("byCardType", C_BYTE),  # 卡类型：1- 普通卡，3- 非授权名单卡，4- 巡更卡，5- 胁迫卡，6- 超级卡，7- 来宾卡，8- 解除卡，为0表示无效
        ("byAllowListNo", C_BYTE),  # 授权名单单号，取值范围：1~8，0表示无效
        ("byReportChannel", C_BYTE),  # 报告上传通道：1- 布防上传，2- 中心组1上传，3- 中心组2上传，0表示无效
        ("byCardReaderKind", C_BYTE),  # 读卡器类型：0- 无效，1- IC读卡器，2- 身份证读卡器，3- 二维码读卡器，4- 指纹头
        ("dwCardReaderNo", C_DWORD),  # 读卡器编号，为0表示无效
        ("dwDoorNo", C_DWORD),  # 门编号（或者梯控的楼层编号），为0表示无效（当接的设备为人员通道设备时，门1为进方向，门2为出方向）
        ("dwVerifyNo", C_DWORD),  # 多重卡认证序号，为0表示无效
        ("dwAlarmInNo", C_DWORD),  # 报警输入号，为0表示无效
        ("dwAlarmOutNo", C_DWORD),  # 报警输出号，为0表示无效
        ("dwCaseSensorNo", C_DWORD),  # 事件触发器编号
        ("dwRs485No", C_DWORD),  # RS485通道号，为0表示无效
        ("dwMultiCardGroupNo", C_DWORD),  # 群组编号
        ("wAccessChannel", C_WORD),  # 人员通道号
        ("byDeviceNo", C_BYTE),  # 设备编号，为0表示无效
        ("byDistractControlNo", C_BYTE),  # 分控器编号，为0表示无效
        ("dwEmployeeNo", C_DWORD),  # 工号，为0无效
        ("wLocalControllerID", C_WORD),  # 就地控制器编号，0-门禁主机，1-255代表就地控制器
        ("byInternetAccess", C_BYTE),  # 网口ID：（1-上行网口1,2-上行网口2,3-下行网口1）
        ("byType", C_BYTE),
        # 防区类型，0:即时防区,1-24小时防区,2-延时防区,3-内部防区,4-钥匙防区,5-火警防区,6-周界防区,7-24小时无声防区,
        # 8-24小时辅助防区,9-24小时震动防区,10-门禁紧急开门防区,11-门禁紧急关门防区，0xff-无
        ("byMACAddr", C_BYTE * 6),  # 物理地址，为0无效
        ("bySwipeCardType", C_BYTE),  # 刷卡类型，0-无效，1-二维码
        ("byMask", C_BYTE),  # 是否带口罩：0-保留，1-未知，2-不戴口罩，3-戴口罩
        ("dwSerialNo", C_DWORD),  # 事件流水号，为0无效
        ("byChannelControllerID", C_BYTE),  # 通道控制器ID，为0无效，1-主通道控制器，2-从通道控制器
        ("byChannelControllerLampID", C_BYTE),  # 通道控制器灯板ID，为0无效（有效范围1-255）
        ("byChannelControllerIRAdaptorID", C_BYTE),  # 通道控制器红外转接板ID，为0无效（有效范围1-255）
        ("byChannelControllerIREmitterID", C_BYTE),  # 通道控制器红外对射ID，为0无效（有效范围1-255）
        ("byHelmet", C_BYTE),  # 可选，是否戴安全帽：0-保留，1-未知，2-不戴安全, 3-戴安全帽
        ("byRes", C_BYTE * 3)]  # 保留，置为0


LPNET_DVR_ACS_EVENT_INFO = POINTER(NET_DVR_ACS_EVENT_INFO)


class NET_DVR_ACS_EVENT_INFO_EXTEND(Structure):
    _fields_ = [
        ("dwFrontSerialNo", C_DWORD),  # 事件流水号，为0无效
        ("byUserType", C_BYTE),  # 人员类型：0-无效，1-普通人（主人），2-来宾（访客），3-非授权名单人，4-管理员
        ("byCurrentVerifyMode", C_BYTE),  # 读卡器当前验证方式
        ("byCurrentEvent", C_BYTE),  # 是否为实时事件：0-无效，1-是（实时事件），2-否（离线事件）
        ("byPurePwdVerifyEnable", C_BYTE),  # 设备是否支持纯密码认证：0-不支持，1-支持
        ("byEmployeeNo", C_BYTE * 32),
        # 工号（人员ID）（对于设备来说，如果使用了工号（人员ID）字段，byEmployeeNo一定要传递，如果byEmployeeNo可转换为dwEmployeeNo，那么该字段也要传递；对于上层平台或客户端来说，优先解析byEmployeeNo字段，如该字段为空，再考虑解析dwEmployeeNo字段）
        ("byAttendanceStatus", C_BYTE),  # 考勤状态：0-未定义,1-上班，2-下班，3-开始休息，4-结束休息，5-开始加班，6-结束加班
        ("byStatusValue", C_BYTE),  # 考勤状态值
        ("byRes2", C_BYTE * 2),  # 保留，置为0
        ("byUUID", C_BYTE * 36),  # UUID（该字段仅在对接萤石平台过程中才会使用）
        ("byDeviceName", C_BYTE * 64),  # 设备序列号
        ("byRes", C_BYTE * 24),  # 保留，置为0
    ]


LPNET_DVR_ACS_EVENT_INFO_EXTEND = POINTER(NET_DVR_ACS_EVENT_INFO_EXTEND)


# 门禁主机报警信息结构体
class NET_DVR_ACS_ALARM_INFO(Structure):
    _fields_ = [
        ("dwSize", C_DWORD),  # 结构体大小
        ("dwMajor", C_DWORD),  # 报警主类型，具体定义见“Remarks”说明
        ("dwMinor", C_DWORD),  # 报警次类型，次类型含义根据主类型不同而不同，具体定义见“Remarks”说明
        ("struTime", NET_DVR_TIME),  # 报警时间
        ("sNetUser", C_BYTE * 16),  # 网络操作的用户名
        ("struRemoteHostAddr", NET_DVR_IPADDR),  # 远程主机地址
        ("struAcsEventInfo", NET_DVR_ACS_EVENT_INFO),  # 报警信息详细参数
        ("dwPicDataLen", C_DWORD),  # 图片数据大小，不为0是表示后面带数据
        # ("pPicData", c_char_p),  # 图片数据缓冲区
        ("pPicData", POINTER(C_BYTE)),  # 图片数据缓冲区
        ("wInductiveEventType", C_WORD),  # 归纳事件类型，0-无效，客户端判断该值为非0值后，报警类型通过归纳事件类型区分，否则通过原有报警主次类型（dwMajor、dwMinor）区分
        ("byPicTransType", C_BYTE),  # 图片数据传输方式: 0-二进制；1-url
        ("byRes1", C_BYTE),  # 保留，置为0
        ("dwIOTChannelNo", C_DWORD),  # IOT通道号
        ("pAcsEventInfoExtend", c_void_p),  # byAcsEventInfoExtend为1时，表示指向一个NET_DVR_ACS_EVENT_INFO_EXTEND结构体
        ("byAcsEventInfoExtend", C_BYTE),  # pAcsEventInfoExtend是否有效：0-无效，1-有效
        ("byTimeType", C_BYTE),  # 时间类型：0-设备本地时间，1-UTC时间（struTime的时间）
        ("byRes2", C_BYTE),  # 保留，置为0
        ("byAcsEventInfoExtendV20", C_BYTE),  # pAcsEventInfoExtendV20是否有效：0-无效，1-有效
        ("pAcsEventInfoExtendV20", c_void_p),  # byAcsEventInfoExtendV20为1时，表示指向一个NET_DVR_ACS_EVENT_INFO_EXTEND_V20结构体
        ("byRes", C_BYTE * 4)  # 保留，置为0
    ]


LPNET_DVR_ACS_ALARM_INFO = POINTER(NET_DVR_ACS_ALARM_INFO)


# 点坐标参数结构体
class NET_VCA_POINT(Structure):
    _fields_ = [
        ("fX", c_float),
        ("fY", c_float)
    ]


# 身份证刷卡信息扩展参数
class NET_DVR_ID_CARD_INFO_EXTEND(Structure):
    _fields_ = [
        ("byRemoteCheck", C_BYTE),
        ("byThermometryUnit", C_BYTE),
        ("byIsAbnomalTemperature", C_BYTE),
        ("byRes2", C_BYTE),
        ("fCurrTemperature", c_float),
        ("struRegionCoordinates", NET_VCA_POINT),
        ("dwQRCodeInfoLen", C_DWORD),
        ("dwVisibleLightDataLen", C_DWORD),
        ("dwThermalDataLen", C_DWORD),
        ("pQRCodeInfo", c_char_p),
        ("pVisibleLightData", c_char_p),
        ("pThermalData", c_char_p),
        ("wXCoordinate", C_WORD),
        ("wYCoordinate", C_WORD),
        ("wWidth", C_WORD),
        ("wHeight", C_WORD),
        ("byHealthCode", C_BYTE),
        ("byNADCode", C_BYTE),
        ("byTravelCode", C_BYTE),
        ("byVaccineStatus", C_BYTE),
        ("byRes", C_BYTE * 1012)
    ]


# 日期信息结构体
class NET_DVR_DATE(Structure):
    _fields_ = [
        ('wYear', C_WORD),
        ('byMonth', C_BYTE),
        ('byDay', C_BYTE)
    ]


# 身份证信息结构体
class NET_DVR_ID_CARD_INFO(Structure):
    _fields_ = [
        ("dwSize", C_DWORD),
        ("byName", C_BYTE * 128),
        ("struBirth", NET_DVR_DATE),
        ("byAddr", C_BYTE * 280),
        ("byIDNum", C_BYTE * 32),
        ("byIssuingAuthority", C_BYTE * 128),
        ("struStartDate", NET_DVR_DATE),
        ("struEndDate", NET_DVR_DATE),
        ("byTermOfValidity", C_BYTE),
        ("bySex", C_BYTE),
        ("byNation", C_BYTE),
        ("byRes", C_BYTE * 101)
    ]


# 时间参数结构体
class NET_DVR_TIME(Structure):
    _fields_ = [
        ("dwYear", C_DWORD),
        ("dwMonth", C_DWORD),
        ("dwDay", C_DWORD),
        ("dwHour", C_DWORD),
        ("dwMinute", C_DWORD),
        ("dwSecond", C_DWORD)
    ]


# 时间参数结构体
class NET_DVR_TIME_V30(Structure):
    _fields_ = [
        ('wYear', C_WORD),
        ('byMonth', C_BYTE),
        ('byDay', C_BYTE),
        ('byHour', C_BYTE),
        ('byMinute', C_BYTE),
        ('bySecond', C_BYTE),
        ('byISO8601', C_BYTE),
        ('wMilliSec', C_WORD),
        ('cTimeDifferenceH', c_byte),
        ('cTimeDifferenceM', c_byte),
    ]


# 身份证刷卡信息上传结构体
class NET_DVR_ID_CARD_INFO_ALARM(Structure):
    _fields_ = [
        ("dwSize", C_DWORD),  # 结构长度
        ("struIDCardCfg", NET_DVR_ID_CARD_INFO),  # 身份证信息
        ("dwMajor", C_DWORD),  # 报警主类型，参考宏定义
        ("dwMinor", C_DWORD),  # 报警次类型，参考宏定义
        ("struSwipeTime", NET_DVR_TIME_V30),  # 刷卡时间
        ("byNetUser", C_BYTE * 16),  # 网络操作的用户名
        ("struRemoteHostAddr", NET_DVR_IPADDR),  # 远程主机地址
        ("dwCardReaderNo", C_DWORD),  # 读卡器编号，为0无效
        ("dwDoorNo", C_DWORD),  # 门编号，为0无效
        ("dwPicDataLen", C_DWORD),  # 图片数据大小，不为0是表示后面带数据
        ("pPicData", c_void_p),  # 身份证图片数据缓冲区，dwPicDataLen不为0时缓冲区里面存放身份证头像的图片数据
        ("byCardType", C_BYTE),  # 卡类型，1-普通卡，3-非授权名单卡，4-巡更卡，5-胁迫卡，6-超级卡，7-来宾卡，8-解除卡，为0无效
        ("byDeviceNo", C_BYTE),  # 设备编号，为0时无效（有效范围1-255）
        ("byMask", C_BYTE),  # 是否带口罩：0-保留，1-未知，2-不戴口罩，3-戴口罩
        ("byRes2", C_BYTE),  # 保留，置为0
        ("dwFingerPrintDataLen", C_DWORD),  # 指纹数据大小，不为0是表示后面带数据
        ("pFingerPrintData", c_void_p),  # 指纹数据缓冲区，dwFingerPrintDataLen不为0时缓冲区里面存放指纹数据
        ("dwCapturePicDataLen", C_DWORD),  # 抓拍图片数据大小，不为0是表示后面带数据
        ("pCapturePicData", c_void_p),  # 抓拍图片数据缓冲区，dwCapturePicDataLen不为0时缓冲区里面存放设备上摄像机抓拍上传的图片数据
        ("dwCertificatePicDataLen", C_DWORD),  # 证件抓拍图片数据大小，不为0是表示后面带数据
        ("pCertificatePicData", c_void_p),  # 证件抓拍图片数据缓冲区，dwCertificatePicDataLen不为0时缓冲区里面存放设备上摄像机抓拍上传的证件抓拍图片数据
        ("byCardReaderKind", C_BYTE),  # 读卡器属于哪一类：0-无效，1-IC读卡器，2-身份证读卡器，3-二维码读卡器，4-指纹头
        ("byRes3", C_BYTE * 2),  # 保留，置为0
        ("byIDCardInfoExtend", C_BYTE),  # pIDCardInfoExtend是否有效：0-无效，1-有效
        ("pIDCardInfoExtend", POINTER(NET_DVR_ID_CARD_INFO_EXTEND)),  # 身份证刷卡扩展事件信息
        ("byRes", C_BYTE * 172)  # 身份证刷卡扩展事件信息
    ]


LPNET_DVR_ID_CARD_INFO_ALARM = POINTER(NET_DVR_ID_CARD_INFO_ALARM)


class NET_DVR_ALARM_ISAPI_PICDATA(Structure):
    _fields_ = [
        ("dwPicLen", C_DWORD),  # 图片数据长度
        ("byPicType", C_BYTE),  # 图片格式: 1- jpg
        ("byRes", C_BYTE * 3),  #
        ("szFilename", c_char * 256),  # 图片名称
        ("pPicData", POINTER(C_BYTE)),  # 图片数据
    ]


LPNET_DVR_ALARM_ISAPI_PICDATA = POINTER(NET_DVR_ALARM_ISAPI_PICDATA)


class NET_DVR_ALARM_ISAPI_INFO(Structure):
    _fields_ = [
        ("pAlarmData", c_char_p),  # 报警数据
        ("dwAlarmDataLen", C_DWORD),  # 报警数据长度
        ("byDataType", C_BYTE),  # 0-invalid,1-xml,2-json
        ("byPicturesNumber", C_BYTE),  # 图片数量
        ("byRes[2]", C_BYTE * 2),  # 保留字节
        ("pPicPackData", c_void_p),  # 图片变长部分
        ("byRes1[32]", C_BYTE * 32),  # 保留字节
    ]


LPNET_DVR_ALARM_ISAPI_INFO = POINTER(NET_DVR_ALARM_ISAPI_INFO)


class NET_DVR_LOCAL_GENERAL_CFG(Structure):
    _fields_ = [
        ("byExceptionCbDirectly", C_BYTE),  # 0-通过线程池异常回调，1-直接异常回调给上层
        ("byNotSplitRecordFile", C_BYTE),  # 回放和预览中保存到本地录像文件不切片 0-默认切片，1-不切片
        ("byResumeUpgradeEnable", C_BYTE),  # 断网续传升级使能，0-关闭（默认），1-开启
        ("byAlarmJsonPictureSeparate", C_BYTE),  # 控制JSON透传报警数据和图片是否分离，0-不分离，1-分离（分离后走COMM_ISAPI_ALARM回调返回）
        ("byRes", C_BYTE * 4),  # 保留
        ("i64FileSize", C_UINT64),  # 单位：Byte
        ("dwResumeUpgradeTimeout", C_DWORD),  # 断网续传重连超时时间，单位毫秒
        ("byAlarmReconnectMode", C_BYTE),  # 0-独立线程重连（默认） 1-线程池重连
        ("byStdXmlBufferSize", C_BYTE),  # 设置ISAPI透传接收缓冲区大小，1-1M 其他-默认
        ("byMultiplexing", C_BYTE),  # 0-普通链接（非TLS链接）关闭多路复用，1-普通链接（非TLS链接）开启多路复用
        ("byFastUpgrade", C_BYTE),  # 0-正常升级，1-快速升级
        ("byRes1", C_BYTE * 232),  # 预留
    ]


# 区域框参数结构体。
class NET_VCA_RECT(Structure):
    _fields_ = [
        ("fX", c_float),  # 边界框左上角点的X轴坐标
        ("fY", c_float),  # 边界框左上角点的Y轴坐标
        ("fWidth", c_float),  # 边界框的宽度
        ("fHeight", c_float)  # 边界框的高度
    ]


# 报警目标信息结构体。
class NET_VCA_TARGET_INFO(Structure):
    _field_ = [
        ('dwID', C_DWORD),  # 目标ID
        ('struRect', NET_VCA_RECT),  # 目标边界框
        ('byRes', C_BYTE * 4)
    ]


# 前端设备信息结构体。
class NET_VCA_DEV_INFO(Structure):
    _fields_ = [
        ('struDevIP', NET_DVR_IPADDR),  # 报警通道对应设备的IP地址
        ('wPort', C_WORD),  # 报警通道对应设备的端口号
        ('byChannel', C_BYTE),  # 报警通道对应设备的通道号，参数值即表示通道号。比如，byChannel=1，表示通道1
        ('byIvmsChannel', C_BYTE)  # SDK接入设备的通道号
    ]


# 人体属性参数结构体。
class NET_VCA_HUMAN_FEATURE(Structure):
    _fields_ = [
        ("byAgeGroup", C_BYTE),  # 年龄段，0xffffffff表示全部（不关注年龄段），详见枚举类型：HUMAN_AGE_GROUP_ENUM
        ("bySex", C_BYTE),  # 性别：1- 男，2- 女
        ("byEyeGlass", C_BYTE),  # 是否戴眼镜：1- 不戴，2- 戴
        ("byAge", C_BYTE),  # 年龄
        ("byAgeDeviation", C_BYTE),  # 年龄误差值，如byAge为15、byAgeDeviation为1，表示实际人脸图片年龄的为14~16之间
        ("byRes0", C_BYTE),  # 保留
        ("byMask", C_BYTE),  # 是否戴口罩：0-表示“未知”（算法不支持）；1- 不戴口罩；2-戴口罩；0xff-算法支持，但是没有识别出来
        ("bySmile", C_BYTE),  # 是否微笑：0-表示“未知”（算法不支持）；1- 不微笑；2- 微笑；0xff-算法支持，但是没有识别出来
        ("byFaceExpression", C_BYTE),  # 保留
        ("byRes1", C_BYTE),  # 保留
        ("byRes2", C_BYTE),  # 保留
        ("byHat", C_BYTE),  # 帽子：0- 不支持；1- 不戴帽子；2- 戴帽子；0xff- 未知,算法支持未检出
        ("byRes", C_BYTE * 4)  # 保留
    ]


# 人脸抓拍结果结构体。
class NET_VCA_FACESNAP_RESULT(Structure):
    _fields_ = [
        ("dwSize", C_DWORD),  # 结构体大小
        ("dwRelativeTime", C_DWORD),  # 相对时标
        ("dwAbsTime", C_DWORD),  # 绝对时标
        ("dwFacePicID", C_DWORD),  # 人脸图ID
        ("dwFaceScore", C_DWORD),  # 人脸评分，范围：0~100
        ("struTargetInfo", NET_VCA_TARGET_INFO),  # 报警目标信息
        ("struRect", NET_VCA_RECT),  # 人脸子图区域
        ("struDevInfo", NET_VCA_DEV_INFO),  # 前端设备信息
        ("dwFacePicLen", C_DWORD),  # 人脸子图的长度，为0表示没有图片，大于0表示有图片
        ("dwBackgroundPicLen", C_DWORD),  # 背景图的长度，为0表示没有图片，大于0表示有图片(保留)
        ("bySmart", C_BYTE),  # 0- iDS设备返回（默认值），1- SMART设备返回
        ("byAlarmEndMark", C_BYTE),  # 报警结束标记：0- 保留，1- 结束标记（该字段结合人脸ID字段使用，表示该ID对应的下报警结束，用于判断报警结束，提取识别图片数据中，清晰度最高的图片）
        ("byRepeatTimes", C_BYTE),  # 重复报警次数：0-无意义
        ("byUploadEventDataType", C_BYTE),  # 人脸图片数据长传方式：0-二进制数据，1-URL
        ("struFeature", NET_VCA_HUMAN_FEATURE),  # 人体属性
        ("fStayDuration", c_float),  # 停留画面中时间（单位：秒）
        ("sStorageIP", c_char * 16),  # 存储服务IP地址
        ("wStoragePort", C_WORD),  # 存储服务端口号
        ("wDevInfoIvmsChannelEx", C_WORD),
        # 与NET_VCA_DEV_INFO里的byIvmsChannel含义相同，能表示更大的值。老客户端用byIvmsChannel能继续兼容，但是最大到255。新客户端版本请使用wDevInfoIvmsChannelEx
        ("byFacePicQuality", C_BYTE),  # 人脸子图图片质量评估等级，0-低等质量，1-中等质量，2-高等质量；
        ("byUIDLen", C_BYTE),  # 上传报警的标识长度
        ("byLivenessDetectionStatus", C_BYTE),  # 活体检测状态: 0-保留，1-未知(检测失败)，2-非真人人脸
        ("byAddInfo", C_BYTE),  # 附加信息标识位：0-无附加信息，1-有附加信息
        ("pUIDBuffer", POINTER(C_BYTE)),  # 标识指针，byUIDLen为1时有效，通过byUIDLen和pUIDBuffer的内容判断是否是同一次抓拍结果
        ("pAddInfoBuffer", POINTER(C_BYTE)),
        # 附加信息指针，byAddInfo为1时有效，指向NET_VCA_FACESNAP_ADDINFO结构体，指针指向内存大小为固定大小即NET_VCA_FACESNAP_ADDINFO结构体的大小
        ("byTimeDiffFlag", C_BYTE),  # 时差字段是否有效：0-时差无效，1-时差有效
        ("cTimeDifferenceH", c_char),  # 与UTC的时差（小时），-12 ... +14，+表示东区,，byTimeDiffFlag为1时有效
        ("cTimeDifferenceM", c_char),  # 与UTC的时差（分钟），-30, 30, 45，+表示东区，byTimeDiffFlag为1时有效
        ("byBrokenNetHttp", C_BYTE),  # 断网续传标志位：0-非重传数据，1-重传数据
        ("pBuffer1", POINTER(C_BYTE)),  # 人脸子图的图片数据
        ("pBuffer2", POINTER(C_BYTE))  # 背景图的图片数据
    ]


LPNET_VCA_FACESNAP_RESULT = POINTER(NET_VCA_FACESNAP_RESULT)


# 籍贯参数结构体
class NET_DVR_AREAINFOCFG(Structure):
    _fields_ = [
        ("wNationalityID", C_WORD),  # 国籍
        ("wProvinceID", C_WORD),  # 省，dwCode为0时取值详见枚举类型：PROVINCE_CITY_IDX
        ("wCityID", C_WORD),  # 市
        ("wCountyID", C_WORD),  # 县
        ("dwCode", C_DWORD),
        # 国家和地区标准的省份、城市、县级代码，为0表示设备不支持，不为0时wNationalityID、wProvinceID、wCityID、wCountyID取值详见全国各省份城市列表
    ]


# 人员信息结构体
class NET_VCA_HUMAN_ATTRIBUTE(Structure):
    _fields_ = [
        ('bySex', C_BYTE),  # 性别：0- 男，1- 女，0xff- 未知
        ('byCertificateType', C_BYTE),  # 证件类型：0- 身份证，1- 警官证，3- 护照，4- 其他，0xff- 未知
        ('byBirthDate', C_BYTE * 10),  # 出生年月，如：201106
        ('byName', C_BYTE * 32),  # 姓名
        ('struNativePlace', NET_DVR_AREAINFOCFG),  # 籍贯
        ('byCertificateNumber', C_BYTE * 32),  # 证件号
        ('dwPersonInfoExtendLen', C_DWORD),  # 人员标签信息扩展长度
        ('pPersonInfoExtend', POINTER(C_BYTE)),
        # 人员标签信息扩展信息，对应XML数据结构：PersonInfoExtendList，该标签信息可以通过接口(NET_DVR_STDXMLConfig)导入，设备端不做处理，直接在比对上传的时候透传携带该数据信息
        ('byAgeGroup', C_BYTE),  # 年龄段，详见枚举类型：HUMAN_AGE_GROUP_ENUM
        ('byRes2', C_BYTE * 3),  # 保留
        ('pThermalData', POINTER(C_BYTE)),  # 热成像图片指针
    ]


# 黑名单人员信息结构体
class NET_VCA_BLOCKLIST_INFO(Structure):
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小
        ('dwRegisterID', C_DWORD),  # 名单注册ID号（只读）
        ('dwGroupNo', C_DWORD),  # 分组号
        ('byType', C_BYTE),  # 非授权名单标志：0- 全部，1- 授权名单(陌生人报警)，2- 非授权名单(人脸比对报警)
        ('byLevel', C_BYTE),  # 非授权名单等级：0- 全部，1- 低，2- 中，3- 高
        ('byRes1', C_BYTE * 2),  # 保留
        ('struAttribute', NET_VCA_HUMAN_ATTRIBUTE),  # 人员信息
        ('byRemark', C_BYTE * 32),  # 备注信息
        ('dwFDDescriptionLen', C_DWORD),  # 人脸库描述数据长度
        ('pFDDescriptionBuffer', POINTER(C_BYTE)),  # 人脸库描述数据指针，对应XML数据结构：FDDescription
        ('dwFCAdditionInfoLen', C_DWORD),  # 抓拍库附加信息长度
        ('pFCAdditionInfoBuffer', POINTER(C_BYTE)),  # 抓拍库附加信息数据指针，对应XML数据结构：FCAdditionInfo
        ('dwThermalDataLen', C_DWORD),  # 热成像图片长度，对应struAttribute字段中的pThermalData热成像图片数据长度，仅人脸比对事件上报支持
    ]


# 定义 （人脸对比）人脸抓拍信息结构体。
class NET_VCA_FACESNAP_INFO_ALARM(Structure):
    _fields_ = [
        ('dwRelativeTime', C_DWORD),  # 相对时标
        ('dwAbsTime', C_DWORD),  # 绝对时标
        ('dwSnapFacePicID', C_DWORD),  # 抓拍人脸图ID
        ('dwSnapFacePicLen', C_DWORD),  # 抓拍人脸子图的长度，为0表示没有图片，大于0表示有图片
        ('struDevInfo', NET_VCA_DEV_INFO),  # 前端设备信息
        ('byFaceScore', C_BYTE),  # 人脸评分，指人脸子图的质量的评分，取值范围：0~100
        ('bySex', C_BYTE),  # 性别：0- 未知，1- 男，2- 女
        ('byGlasses', C_BYTE),  # 是否带眼镜：0- 未知，1- 是，2- 否
        ('byAge', C_BYTE),  # 年龄
        ('byAgeDeviation', C_BYTE),  # 年龄误差值，如byAge为15且byAgeDeviation为1，则表示实际人脸图片年龄的为14~16之间
        ('byAgeGroup', C_BYTE),  # 年龄段，详见枚举类型：HUMAN_AGE_GROUP_ENUM
        ('byFacePicQuality', C_BYTE),
        # 脸子图图片质量评估等级：0-低等质量，1-中等质量，2-高等质量，该质量评估算法仅针对人脸子图单张图片，具体是通过姿态、清晰度、遮挡情况、光照情况等可影响人脸抓拍性能的因素综合评估的结果
        ('byRes', C_BYTE),  # 保留
        ('dwUIDLen', C_DWORD),  # 上传报警的标识长度
        ('pUIDBuffer', POINTER(C_BYTE)),  # 缓冲区指针，存放上传报警的标识信息，信息相同表示同一次报警上传的结果
        ('fStayDuration', c_float),  # 停留画面中时间(单位：秒)
        ('pBuffer1', POINTER(C_BYTE)),  # 抓拍人脸子图的图片数据
    ]


# 非授权名单报警信息结构体。
class NET_VCA_BLOCKLIST_INFO_ALARM(Structure):
    _fields_ = [
        ('struBlockListInfo', NET_VCA_BLOCKLIST_INFO),  # 非授权名单基本信息
        ('dwBlockListPicLen', C_DWORD),  # 非授权名单人脸子图的长度，为0表示没有图片，大于0表示有图片
        ('dwFDIDLen', C_DWORD),  # 人脸库ID长度
        ('pFDID', POINTER(C_BYTE)),  # 人脸库ID数据缓冲区指针
        ('dwPIDLen', C_DWORD),  # 人脸库图片ID长度
        ('pPID', POINTER(C_BYTE)),  # 人脸库图片ID指针
        ('wThresholdValue', C_WORD),  # 人脸库阈值，取值范围：[0,100]
        ('byRes', C_BYTE * 2),  # 保留
        ('pBuffer1', POINTER(C_BYTE)),  # 非授权名单人脸子图的图片数据
    ]  # 人脸比对报警信息


# 人脸对比参数结构体
class NET_VCA_FACESNAP_MATCH_ALARM(Structure):
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小
        ('fSimilarity', c_float),  # 相似度，取值范围：[0.001,1]
        ('struSnapInfo', NET_VCA_FACESNAP_INFO_ALARM),  # 人脸抓拍上传信息
        ('struBlockListInfo', NET_VCA_BLOCKLIST_INFO_ALARM),  # 人脸比对报警信息
        ('sStorageIP', c_char * 16),  # 存储服务IP地址
        ('wStoragePort', C_WORD),  # 存储服务端口号
        ('byMatchPicNum', C_BYTE),  # 匹配图片的数量，0是保留值（不支持该字段的设备，该值默认为0；支持该字段的设备，该值为0时表示后续没有匹配的图片信息）
        ('byPicTransType', C_BYTE),  # 图片数据传输方式: 0- 二进制，1- URL路径(HTTP协议的图片URL)
        ('dwSnapPicLen', C_DWORD),  # 设备识别抓拍图片长度
        ('pSnapPicBuffer', POINTER(C_BYTE)),  # 设备识别抓拍图片指针
        ('struRegion', NET_VCA_RECT),  # 设备识别抓拍图片中人脸子图坐标，可以根据该坐标从抓拍图片上抠取人脸小图片
        ('dwModelDataLen', C_DWORD),  # 建模数据长度
        ('pModelDataBuffer', POINTER(C_BYTE)),  # 建模数据指针
        ('byModelingStatus', C_BYTE),  # 建模状态
        ('byLivenessDetectionStatus', C_BYTE),  # 活体检测状态：0-保留，1-未知（检测失败），2-非真人人脸，3-真人人脸，4-未开启活体检测
        ('cTimeDifferenceH', c_char),  # 与UTC的时差（小时），-12 ... +14，+表示东区，0xff无效
        ('cTimeDifferenceM', c_char),  # 与UTC的时差（分钟），-30, 30, 45，+表示东区，0xff无效
        ('byMask', C_BYTE),  # 抓拍图是否戴口罩，0-保留，1-未知，2-不戴口罩，3-戴口罩
        ('bySmile', C_BYTE),  # 抓拍图是否微笑，0-保留，1-未知，2-不微笑，3-微笑
        ('byContrastStatus', C_BYTE),  # 比对结果，0-保留，1-比对成功，2-比对失败
        ('byBrokenNetHttp', C_BYTE),  # 断网续传标志位：0- 不是重传数据，1- 重传数据
    ]


LPNET_DVR_LOCAL_GENERAL_CFG = POINTER(NET_DVR_LOCAL_GENERAL_CFG)


# 以太网配置结构体。
class NET_DVR_ETHERNET(Structure):
    _fields_ = [
        ('sDVRIP', c_char * 16),  # 设备IP地址
        ('sDVRIPMask', c_char * 16),  # 设备IP地址掩码
        ('dwNetInterface', C_DWORD),  # 网络接口：1-10MBase-T；2-10MBase-T全双工；3-100MBase-TX；4-100M全双工；5-10M/100M自适应
        ('wDVRPort', C_WORD),  # 设备端口号
        ('byMACAddr', C_BYTE * 6)  # 设备物理地址
    ]


# 网络配置结构体。
class NET_DVR_NETCFG(Structure):
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小
        ('struEtherNet', NET_DVR_ETHERNET * 2),  # 以太网口
        ('sManageHostIP', c_char * 16),  # 远程管理主机地址
        ('wManageHostPort', C_WORD),  # 远程管理主机端口号
        ('sIPServerIP', c_char * 16),  # IPServer服务器地址
        ('sMultiCastIP', c_char * 16),  # 多播组地址
        ('sGatewayIP', c_char * 16),  # 网关地址
        ('sNFSIP', c_char * 16),  # NFS主机IP地址
        ('sNFSDirectory', C_BYTE * 128),  # NFS目录
        ('dwPPPOE', C_DWORD),  # 0-不启用,1-启用
        ('sPPPoEUser', C_BYTE * 32),  # PPPoE用户名
        ('sPPPoEPassword', c_char * 16),  # PPPoE密码
        ('sPPPoEIP', c_char * 16),  # PPPoE IP地址(只读)
        ('wHttpPort', C_WORD)  # HTTP端口号
    ]


LPNET_DVR_NETCFG = POINTER(NET_DVR_NETCFG)


# 以太网配置结构体。
class NET_DVR_ETHERNET_V30(Structure):
    _fields_ = [
        ('struDVRIP', NET_DVR_IPADDR),  # 设备IP地址
        ('struDVRIPMask', NET_DVR_IPADDR),  # 设备IP地址掩码
        ('dwNetInterface', C_DWORD),
        # 网络接口：1-10MBase-T；2-10MBase-T全双工；3-100MBase-TX；4-100M全双工；5-10M/100M/1000M自适应；6-1000M全双工
        ('wDVRPort', C_WORD),  # 设备端口号
        ('wMTU', C_WORD),  # MTU设置，默认1500
        ('byMACAddr', C_BYTE * 6),  # 设备物理地址
        ('byEthernetPortNo', C_BYTE),  # 网口号，0-无效，1-网口0，2-网口1以此类推，只读
        ('byRes', C_BYTE * 1),
    ]


# PPPoE配置结构体。
class NET_DVR_PPPOECFG(Structure):
    _fields_ = [
        ('dwPPPOE', C_DWORD),  # 是否启用PPPoE：0-不启用，1-启用
        ('sPPPoEUser', C_BYTE * 32),  # PPPoE用户名
        ('sPPPoEPassword', c_char * 16),  # PPPoE密码
        ('struPPPoEIP', NET_DVR_IPADDR),  # PPPoE IP地址
    ]


# 网络配置结构体。
class NET_DVR_NETCFG_V50(Structure):
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小
        ('struEtherNet', NET_DVR_ETHERNET_V30 * 2),  # 以太网口
        ('struRes1', NET_DVR_IPADDR * 2),  #
        ('struAlarmHostIpAddr', NET_DVR_IPADDR),  #
        ('byRes2', C_BYTE * 4),  #
        ('wAlarmHostIpPort', C_WORD),  # 报警主机端口号
        ('byUseDhcp', C_BYTE),  # 是否启用DHCP 0xff-无效 0-不启用 1-启用
        ('byIPv6Mode', C_BYTE),  # IPv6分配方式，0-路由公告，1-手动设置，2-启用DHCP分配
        ('struDnsServer1IpAddr', NET_DVR_IPADDR),  # 域名服务器1的IP地址
        ('struDnsServer2IpAddr', NET_DVR_IPADDR),  # 域名服务器2的IP地址
        ('byIpResolver', C_BYTE * 64),  # IP解析服务器域名或IP地址
        ('wIpResolverPort', C_WORD),  # IP解析服务器端口号
        ('wHttpPortNo', C_WORD),  # HTTP端口号
        ('struMulticastIpAddr', NET_DVR_IPADDR),  # 多播组地址
        ('struGatewayIpAddr', NET_DVR_IPADDR),  # 网关地址
        ('struPPPoE', NET_DVR_PPPOECFG),  #
        ('byEnablePrivateMulticastDiscovery', C_BYTE),  # 私有多播搜索，0~默认，1~启用，2-禁用
        ('byEnableOnvifMulticastDiscovery', C_BYTE),  # Onvif多播搜索，0~默认，1~启用，2-禁用
        ('wAlarmHost2IpPort', C_WORD),  # 报警主机2端口号
        ('struAlarmHost2IpAddr', NET_DVR_IPADDR),  # 报警主机2 IP地址
        ('byEnableDNS', C_BYTE),  # DNS使能, 0-关闭，1-打开
        ('byRes', C_BYTE * 599),  # DNS使能, 0-关闭，1-打开
    ]


# 定义预览参数结构体
class NET_DVR_PREVIEWINFO(Structure):
    _fields_ = [
        ('lChannel', C_LONG),  # 通道号
        ('dwStreamType', C_DWORD),  # 码流类型，0-主码流，1-子码流，2-码流3，3-码流4, 4-码流5,5-码流6,7-码流7,8-码流8,9-码流9,10-码流10
        ('dwLinkMode', C_DWORD),
        # 0：TCP方式,1：UDP方式,2：多播方式,3 - RTP方式，4-RTP/RTSP,5-RSTP/HTTP ,6- HRUDP（可靠传输） ,7-RTSP/HTTPS
        ('hPlayWnd', C_HWND),  # 播放窗口的句柄,为NULL表示不播放图象
        ('bBlocked', C_BOOL),  # 0-非阻塞取流, 1-阻塞取流, 如果阻塞SDK内部connect失败将会有5s的超时才能够返回,不适合于轮询取流操作
        ('bPassbackRecord', C_BOOL),  # 0-不启用录像回传,1启用录像回传
        ('byPreviewMode', C_BYTE),  # 预览模式，0-正常预览，1-延迟预览
        ('byStreamID', C_BYTE * 32),  # 流ID，lChannel为0xffffffff时启用此参数
        ('byProtoType', C_BYTE),  # 应用层取流协议，0-私有协议，1-RTSP协议,
        # 2-SRTP码流加密（对应此结构体中dwLinkMode 字段，支持如下方式, 为1，表示udp传输方式，信令走TLS加密，码流走SRTP加密，为2，表示多播传输方式，信令走TLS加密，码流走SRTP加密）
        ('byRes1', C_BYTE),
        ('byVideoCodingType', C_BYTE),  # 码流数据编解码类型 0-通用编码数据 1-热成像探测器产生的原始数据
        ('dwDisplayBufNum', C_DWORD),  # 播放库播放缓冲区最大缓冲帧数，范围1-50，置0时默认为1
        ('byNPQMode', C_BYTE),  # NPQ是直连模式，还是过流媒体：0-直连 1-过流媒体
        ('byRecvMetaData', C_BYTE),  # 是否接收metadata数据
        # 设备是否支持该功能通过GET /ISAPI/System/capabilities 中DeviceCap.SysCap.isSupportMetadata是否存在且为true
        ('byDataType', C_BYTE),  # 数据类型，0-码流数据，1-音频数据
        ('byRes', C_BYTE * 213),
    ]


LPNET_DVR_PREVIEWINFO = POINTER(NET_DVR_PREVIEWINFO)

# 报警信息回调函数
MSGCallBack_V31 = fun_ctype(c_bool, C_LONG, LPNET_DVR_ALARMER, c_void_p, C_DWORD, c_void_p)

# 码流回调函数
REALDATACALLBACK = fun_ctype(None, C_LONG, C_DWORD, POINTER(C_BYTE), C_DWORD, c_void_p)
