# hikvision-sdk-python
Place Hikvision SDK DLLs in lib/ directory:

HCNetSDK.dll

PlayCtrl.dll

libcrypto-1_1-x64.dll

libssl-1_1-x64.dll

API Reference
HKCam(camIP, username, password, devport=8000)
Initialize connection to Hikvision camera.

Parameters:

camIP: Camera IP address

username: Login username

password: Login password

devport: Device port (default: 8000)

read()
Read next frame from camera.

Returns:

timestamp: Frame timestamp

frame: RGB image as numpy array

release()
Release all resources and logout from camera.

Examples
See the examples directory for:

Basic video streaming

Video recording

Motion detection

Integration with OpenCV

Troubleshooting
Common Issues
DLL loading errors: Ensure all required DLLs are in the lib/ directory

Login failures: Verify camera IP, username and password

Video streaming issues: Check network connection and camera status

Error Codes
Refer to Hikvision SDK documentation for error code meanings.

License
MIT License - See LICENSE for details.

Contributing
Pull requests are welcome! Please ensure:

Code follows PEP 8 style guide

New features include tests

Documentation is updated

Acknowledgements
Hikvision for their SDK

OpenCV and NumPy communities