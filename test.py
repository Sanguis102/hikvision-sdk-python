# coding=utf-8
import os
import time
import cv2
import ctypes
import numpy as np
import psutil # Importa psutil para medir o uso da CPU
from queue import Queue # Importa a fila para comunicação entre threads

from HCNetSDK import *
from PlayCtrl import *

class HKCamOptimized(object):
    def __init__(self, camIP, username, password, devport=8000):
        self.DEV_IP = create_string_buffer(camIP.encode())
        self.DEV_PORT = devport
        self.DEV_USER_NAME = create_string_buffer(username.encode())
        self.DEV_PASSWORD = create_string_buffer(password.encode())
        
        # --- OTIMIZAÇÃO: Usa uma fila para quadros ---
        # A fila armazena (buffer_yuv, largura, altura)
        self.frame_queue = Queue(maxsize=2)
        
        self.lUserId = -1
        self.lRealPlayHandle = -1
        self.PlayCtrl_Port = c_long(-1)

        self.LoadDevSDK()
        self.Objdll.NET_DVR_Init()
        self.Objdll.NET_DVR_SetLogToFile(3, bytes('./SdkLog_Python/', encoding="utf-8"), False)

        (self.lUserId, self.device_info) = self.LoginDev()
        if self.lUserId < 0:
            print(f'Login falhou, erro: {self.Objdll.NET_DVR_GetLastError()}')
            self.Objdll.NET_DVR_Cleanup()
            exit()
        else:
            print(f'Câmera [{camIP}] logada com sucesso!!')
        self.start_play()
        time.sleep(1)

    def LoadDevSDK(self):
        try:
            self.Objdll = ctypes.CDLL(netsdkdllpath)
            self.Playctrldll = ctypes.CDLL(playM4dllpath)
        except OSError as e:
            print(f"Erro ao carregar DLLs: {e}")
            exit(1)
            
    def LoginDev(self):
        device_info = NET_DVR_DEVICEINFO_V30()
        lUserId = self.Objdll.NET_DVR_Login_V30(self.DEV_IP, self.DEV_PORT, self.DEV_USER_NAME, self.DEV_PASSWORD, byref(device_info))
        return (lUserId, device_info)

    def start_play(self):
        if not self.Playctrldll.PlayM4_GetPort(byref(self.PlayCtrl_Port)):
            print(u'Falha ao obter porta da biblioteca de reprodução')
            return

        # --- OTIMIZAÇÃO: O callback é mantido como um membro da classe para evitar que seja coletado pelo garbage collector ---
        self.funcRealDataCallBack_V30 = REALDATACALLBACK(self.RealDataCallBack_V30)
        preview_info = NET_DVR_PREVIEWINFO()
        preview_info.hPlayWnd = 0
        preview_info.lChannel = 1
        preview_info.dwStreamType = 1 # Sub-stream para menor latência
        preview_info.dwLinkMode = 0
        preview_info.bBlocked = 1

        self.lRealPlayHandle = self.Objdll.NET_DVR_RealPlay_V40(self.lUserId, byref(preview_info), self.funcRealDataCallBack_V30, None)
        if self.lRealPlayHandle < 0:
            print(f'Falha ao iniciar o preview, erro: {self.Objdll.NET_DVR_GetLastError()}')
            self.release()
            exit()
        
        self.Playctrldll.PlayM4_SetDisplayBuf(self.PlayCtrl_Port, 1)

    def RealDataCallBack_V30(self, lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
        if dwDataType == NET_DVR_SYSHEAD:
            if self.Playctrldll.PlayM4_OpenStream(self.PlayCtrl_Port, pBuffer, dwBufSize, 1024 * 1024):
                self.FuncDecCB = DECCBFUNWIN(self.DecCBFun)
                self.Playctrldll.PlayM4_SetDecCallBackExMend(self.PlayCtrl_Port, self.FuncDecCB, None, 0, None)
                if not self.Playctrldll.PlayM4_Play(self.PlayCtrl_Port, None):
                    print(u'PlayM4_Play falhou')
            else:
                print(u'PlayM4_OpenStream falhou')
        elif dwDataType == NET_DVR_STREAMDATA:
            self.Playctrldll.PlayM4_InputData(self.PlayCtrl_Port, pBuffer, dwBufSize)

    def DecCBFun(self, nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2):
        # --- OTIMIZAÇÃO: Callback faz o mínimo de trabalho possível ---
        if pFrameInfo.contents.nType == 3: # T_YV12
            # Apenas copia os dados brutos e os coloca na fila
            pFrameInfo_contents = pFrameInfo.contents
            if not self.frame_queue.full():
                # Copia os dados para um novo buffer para que o SDK possa reutilizar o original
                frame_data = ctypes.string_at(pBuf, nSize)
                self.frame_queue.put((frame_data, pFrameInfo_contents.nWidth, pFrameInfo_contents.nHeight))

    def read(self):
        # --- OTIMIZAÇÃO: Leitura eficiente bloqueando na fila ---
        try:
            # Bloqueia por no máximo 1 segundo
            yuv_data, width, height = self.frame_queue.get(timeout=1)
            
            # --- OTIMIZAÇÃO: Conversão de cor movida para o thread consumidor ---
            YUV = np.frombuffer(yuv_data, dtype=np.uint8).reshape((height * 3 // 2, width))
            img_bgr = cv2.cvtColor(YUV, cv2.COLOR_YUV2BGR_YV12)
            return img_bgr
        except Exception:
            # Retorna None se a fila estiver vazia por muito tempo
            return None

    def release(self):
        # --- OTIMIZAÇÃO: Lógica de liberação de recursos mais robusta ---
        if self.lRealPlayHandle >= 0:
            self.Objdll.NET_DVR_StopRealPlay(self.lRealPlayHandle)
        if self.PlayCtrl_Port.value > -1:
            self.Playctrldll.PlayM4_Stop(self.PlayCtrl_Port)
            self.Playctrldll.PlayM4_CloseStream(self.PlayCtrl_Port)
            self.Playctrldll.PlayM4_FreePort(self.PlayCtrl_Port)
            self.PlayCtrl_Port = c_long(-1)
        if self.lUserId >= 0:
            self.Objdll.NET_DVR_Logout(self.lUserId)
        self.Objdll.NET_DVR_Cleanup()
        print('Recursos liberados (otimizado).')


if __name__ == "__main__":
    # --- CONFIGURAÇÕES ---
    CAM_IP = '192.168.5.220'
    CAM_USER = 'admin'
    CAM_PASS = 'glp33068'
    
    HIK = HKCamOptimized(CAM_IP, CAM_USER, CAM_PASS)
    
    # --- MEDIÇÃO DE PERFORMANCE ---
    process = psutil.Process(os.getpid())
    frame_count = 0
    start_time = time.time()
    
    while True:
        try:
            img = HIK.read()
            if img is not None:
                frame_count += 1
                
                if frame_count % 30 == 0:
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    fps = frame_count / elapsed_time
                    cpu_usage = process.cpu_percent() / psutil.cpu_count()
                    
                    print(f"--- Otimizado --- FPS: {fps:.2f}, CPU: {cpu_usage:.2f}%, Fila: {HIK.frame_queue.qsize()}")
                    
                    frame_count = 0
                    start_time = time.time()

                cv2.imshow("Otimizado - CPU BAIXO", img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            break
            
    HIK.release()
    cv2.destroyAllWindows()
