# coding=utf-8
import os
import platform
from HCNetSDK import *
from PlayCtrl import *
import numpy as np
import time
import cv2  # 确保已导入cv2模块
import ctypes  # 用于加载DLL文件


class HKCam(object):
    def __init__(self, camIP, username, password, devport=8000):
        # 登录的设备信息
        self.DEV_IP = create_string_buffer(camIP.encode())
        self.DEV_PORT = devport
        self.DEV_USER_NAME = create_string_buffer(username.encode())
        self.DEV_PASSWORD = create_string_buffer(password.encode())
        self.funcRealDataCallBack_V30 = None
        self.recent_img = None  # 最新帧
        self.n_stamp = None  # 帧时间戳
        self.last_stamp = None  # 上次时间戳
        self.PlayCtrl_Port = C_LONG(-1)  # 初始化播放库通道号
        # 加载库,先加载依赖库                                                                   # 1 根据操作系统，加载对应的dll文件
        self.LoadDevSDK()
        # 设置组件库和SSL库加载路径                                                              # 2 设置组件库和SSL库加载路径
        self.SetSDKInitCfg()
        # 初始化DLL
        self.Objdll.NET_DVR_Init()  # 3 相机初始化
        # 启用SDK写日志
        self.Objdll.NET_DVR_SetLogToFile(3, bytes('./SdkLog_Python/', encoding="utf-8"), False)
        os.chdir(r'../../')  # 切换工作路径到../../
        # 登录
        (self.lUserId, self.device_info) = self.LoginDev()  # 4 登录相机
        self.Playctrldll.PlayM4_ResetBuffer(self.lUserId, 1)  # 清空指定缓冲区的剩余数据。这个地方传进来的是self.lUserId，为什么呢？
        print(self.lUserId)
        if self.lUserId < 0:  # 登录失败
            err = self.Objdll.NET_DVR_GetLastError()
            print('Login device fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
            # 释放资源
            self.Objdll.NET_DVR_Cleanup()
            exit()
        else:
            print(f'摄像头[{camIP}]登录成功!!')
        self.start_play()  # 5 开始播放
        time.sleep(1)

    def start_play(self):
        # 获取一个播放句柄
        if not self.Playctrldll.PlayM4_GetPort(byref(self.PlayCtrl_Port)):
            print(u'获取播放库句柄失败')

        # 定义码流回调函数
        self.funcRealDataCallBack_V30 = REALDATACALLBACK(self.RealDataCallBack_V30)

        # 开启预览
        self.preview_info = NET_DVR_PREVIEWINFO()
        self.preview_info.hPlayWnd = 0
        self.preview_info.lChannel = 1  # 通道号
        self.preview_info.dwStreamType = 1  # 使用子码流降低延迟
        self.preview_info.dwLinkMode = 0  # TCP
        self.preview_info.bBlocked = 1  # 阻塞取流

        # 开始预览并且设置回调函数回调获取实时流数据
        self.lRealPlayHandle = self.Objdll.NET_DVR_RealPlay_V40(self.lUserId, byref(self.preview_info),
                                                                self.funcRealDataCallBack_V30, None)
        if self.lRealPlayHandle < 0:
            print('Open preview fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
            # 登出设备
            self.Objdll.NET_DVR_Logout(self.lUserId)
            # 释放资源
            self.Objdll.NET_DVR_Cleanup()
            exit()
        else:
            # 设置低延迟模式
            self.Playctrldll.PlayM4_SetDisplayBuf(self.PlayCtrl_Port, 1)  # 缓冲区设为1帧

    def SetSDKInitCfg(self):
        # 设置SDK初始化依赖库路径
        strPath = os.getcwd().encode('gbk')
        sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
        sdk_ComPath.sPath = strPath
        print('strPath: ', strPath)

        # 设置SDK路径
        if self.Objdll.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath)):
            print('NET_DVR_SetSDKInitCfg: 2 Succ')

        # 设置加密库路径
        if self.Objdll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'\\libcrypto-1_1-x64.dll')):
            print('NET_DVR_SetSDKInitCfg: 3 Succ')

        # 设置SSL库路径
        if self.Objdll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'\\libssl-1_1-x64.dll')):
            print('NET_DVR_SetSDKInitCfg: 4 Succ')

    def LoginDev(self):
        # 登录注册设备
        device_info = NET_DVR_DEVICEINFO_V30()
        lUserId = self.Objdll.NET_DVR_Login_V30(self.DEV_IP, self.DEV_PORT, self.DEV_USER_NAME, self.DEV_PASSWORD,
                                                byref(device_info))
        return (lUserId, device_info)

    def read(self):
        while self.n_stamp == self.last_stamp:
            continue
        self.last_stamp = self.n_stamp
        return self.n_stamp, self.recent_img

    def DecCBFun(self, nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2):
        if pFrameInfo.contents.nType == 3:
            t0 = time.time()
            # 解码返回视频YUV数据，将YUV数据转成jpg图片保存到本地
            # 如果有耗时处理，需要将解码数据拷贝到回调函数外面的其他线程里面处理，避免阻塞回调导致解码丢帧
            nWidth = pFrameInfo.contents.nWidth
            nHeight = pFrameInfo.contents.nHeight
            # nType = pFrameInfo.contents.nType
            dwFrameNum = pFrameInfo.contents.dwFrameNum
            nStamp = pFrameInfo.contents.nStamp
            # print(nWidth, nHeight, nType, dwFrameNum, nStamp, sFileName)
            YUV = np.frombuffer(pBuf[:nSize], dtype=np.uint8)
            YUV = np.reshape(YUV, [nHeight + nHeight // 2, nWidth])
            img_rgb = cv2.cvtColor(YUV, cv2.COLOR_YUV2BGR_YV12)
            self.recent_img, self.n_stamp = img_rgb, nStamp

    def RealDataCallBack_V30(self, lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
        # 码流回调函数
        if dwDataType == NET_DVR_SYSHEAD:
            # 设置流播放模式
            self.Playctrldll.PlayM4_SetStreamOpenMode(self.PlayCtrl_Port, 0)
            # 打开码流，送入40字节系统头数据
            if self.Playctrldll.PlayM4_OpenStream(self.PlayCtrl_Port, pBuffer, dwBufSize, 1024 * 1024):
                # 设置解码回调，可以返回解码后YUV视频数据
                # global FuncDecCB
                self.FuncDecCB = DECCBFUNWIN(self.DecCBFun)
                self.Playctrldll.PlayM4_SetDecCallBackExMend(self.PlayCtrl_Port, self.FuncDecCB, None, 0, None)
                # 开始解码播放
                if self.Playctrldll.PlayM4_Play(self.PlayCtrl_Port, None):
                    print(u'播放库播放成功')
                else:
                    print(u'播放库播放失败')
            else:
                print(u'播放库打开流失败')
        elif dwDataType == NET_DVR_STREAMDATA:
            self.Playctrldll.PlayM4_InputData(self.PlayCtrl_Port, pBuffer, dwBufSize)
        else:
            print(u'其他数据,长度:', dwBufSize)

    def release(self):
        self.Objdll.NET_DVR_StopRealPlay(self.lRealPlayHandle)
        if self.PlayCtrl_Port.value > -1:
            self.Playctrldll.PlayM4_Stop(self.PlayCtrl_Port)
            self.Playctrldll.PlayM4_CloseStream(self.PlayCtrl_Port)
            self.Playctrldll.PlayM4_FreePort(self.PlayCtrl_Port)
            PlayCtrl_Port = c_long(-1)
            self.Objdll.NET_DVR_Logout(self.lUserId)
            self.Objdll.NET_DVR_Cleanup()
        print('释放资源结束')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def LoadDevSDK(self):
        os.chdir(r'./lib')
        self.Objdll = ctypes.CDLL(r'./HCNetSDK.dll')  # 加载网络库
        self.Playctrldll = ctypes.CDLL(r'./PlayCtrl.dll')  # 加载播放库)


if __name__ == "__main__":
    camIP = '192.168.5.220'
    # camIP ='192.168.3.157'
    DEV_PORT = 8000
    username = 'admin'
    password = 'glp33068'
    HIK = HKCam(camIP, username, password)
    last_stamp = 0
    while True:
        t0 = time.time()
        try:
            n_stamp, img = HIK.read()
            cv2.imshow("Camera Preview", img)  # 显示摄像头画面
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q键退出预览
                break
        except KeyboardInterrupt:
            print("\n程序被用户中断，正在优雅退出...")
            HIK.release()
            cv2.destroyAllWindows()
            exit(0)
    HIK.release()