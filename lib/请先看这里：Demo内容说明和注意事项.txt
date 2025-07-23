【Demo内容说明】
-------------------------------------
1. 接口调用流程：https://open.hikvision.com/docs/docId?productId=5cda567cf47ae80dd41a54b3&version=%2F37a7978a747a454da559febb6e9e26f6&curNodeId=2d4e3a762f4949f8ae85302d1cdee9a1。
2.实时预览取流，取流之后可以使用播放库SDK进行解码显示，播放库SDK下载地址：https://open.hikvision.com/download/5cda567cf47ae80dd41a54b3?type=10&id=f11dc00afd8342ac8996493490d77f57。


【注意事项】
------------------------------------
1. 请到海康威视官网下载最新版本设备网络SDK：https://open.hikvision.com/download/5cda567cf47ae80dd41a54b3?type=10

2. 程序代码中CDLL或LoadLibrary接口中指定SDK动态库的路径，SetSDKInitCfg中设置依赖库加载路径。此Demo在Win和Linux系统下通用，切换到Linux系统则设置为Linux系统的SDK库文件路径。

3. Windows开发时需要将“库文件”文件夹中的HCNetSDK.dll、HCCore.dll、HCNetSDKCom文件夹、libssl-1_1-x64.dll、libcrypto-1_1-x64.dll、hlog.dll、hpr.dll、zlib1.dll等文件拷贝到\lib\win文件夹下，HCNetSDKCom文件夹（包含里面的功能组件dll库文件）需要和HCNetSDK.dll、HCCore.dll一起加载，放在同一个目录下，且HCNetSDKCom文件夹名不能修改。如果自行开发软件不能正常实现相应功能，而且程序没有指定加载的dll库路径，请在程序运行的情况下尝试删除HCNetSDK.dll。如果可以删除，说明程序可能调用到系统盘Windows->System32目录下的dll文件，建议删除或者更新该目录下的相关dll文件；如果不能删除，dll文件右键选择属性确认SDK库版本。

4. Linux开发时需要将“库文件”文件夹中libhcnetsdk.so、libHCCore.so、libcrypto.so.1.1、libssl.so.1.1、libhpr.so、libz.so等文件拷贝到\lib\linux文件夹下。HCNetSDKCom文件夹（包含里面的功能组件dll库文件）需要和libhcnetsdk.so、libHCCore.so一起加载，放在同一个目录下，且HCNetSDKCom文件夹名不能修改。如果库文件加载有问题，初始化失败，也可以尝试将SDK所在路径添加到LD_LIBRARY_PATH环境变量中。
