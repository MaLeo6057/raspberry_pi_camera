# raspberry_pi_camera
本算法为利用树莓派（raspberry pi）配合两个USB摄像头搭建的简易双摄像头图像采集装置。

## python第三方包
pygame
numpy
RPi
cv2
pyexiv2
PIL

## 其他信息
本程序需要四个GPIO按钮，程序中button1为拍摄图像按钮，button2为关闭机器按钮，button3为停止程序回到系统按钮，button4为切换摄像头按钮。
两个摄像头的分辨率默认设为640x480.可在程序中自行修改。
