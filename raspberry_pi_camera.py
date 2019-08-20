import pygame.camera
import numpy as np
import RPi.GPIO as GPIO
import cv2
import time
import datetime
import os
import sys
import base64
import pygame
import pyexiv2 as ev
from pygame.locals import *
from PIL import Image
from subprocess import call

class exif():
    def __init__(self):
        self.Artist = 'HIT'
        self.Software = 'HIT-CAMERA'

    def imgExif(self, path):
        try:
            exiv_image = ev.ImageMetadata(path)
            exiv_image.read()
            exiv_image["Exif.Image.Artist"] = self.Artist
            exiv_image["Exif.Image.Software"] = self.Software
            exiv_image.write()
        except:
            print('failed')

    def star(self):
        global PictureName
        path = PictureName
        self.imgExif(path)
        self.imgExif(PictureName[0:20] + '_en/' + PictureName[21:40])

class double_cam():
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.camera.init()
        self.num = 0
        self.Running = True
        self.flag_switch = True
        self.cam = pygame.camera.Camera("/dev/video0", [640, 480])
        self.cam2 = pygame.camera.Camera("/dev/video1", [640, 480])
        self.cam.start()
        self.cam2.start()

    def Shutdown(self,button2):
        # global Running
        # cambool = self.cam.query_image()
        # if (cambool):
        #     self.cam.stop()
        pygame.quit()
        cmd_shutdown = 'sudo shutdown -h now'
        os.system(cmd_shutdown)
        self.Running = False

    def switch_cam(self,button4):
        # global flag_switch, num
        self.num = self.num + 1
        if (self.flag_switch):
            self.flag_switch = False
        else:
            self.flag_switch = True

    def TakePicture(self,button1):
        global flag
        # if flag = False,Take a picture; if flag = True,back to preview
        flag = False

    def SHUT(self,button3):
        # global Running
        self.Running = False
        # cambool = self.cam.query_image()
        # if (cambool):
        #     self.cam.stop()
        pygame.quit()

    def surface_to_string(self,surface):
        # """convert pygame surface into string"""
        return pygame.image.tostring(surface, 'RGB')

    def pygame_to_cvimage(self,surface):
        """conver pygame surface into  cvimage"""
        image_string = self.surface_to_string(surface)
        image_np = np.fromstring(image_string, np.uint8).reshape(1280, 720, 3)
        frame = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        return image_np, frame

    def run_cam(self):
        os.environ['SDL_FBDEV'] = '/dev/fb1'
        GPIO.setmode(GPIO.BOARD)
        button1 = 36
        button2 = 37  # SHUTDOWN
        button3 = 33
        button4 = 32  # switch cam

        GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        input_value = GPIO.input(button1)
        GPIO.add_event_detect(button3, GPIO.FALLING, callback=self.SHUT, bouncetime=200)
        GPIO.add_event_detect(button1, GPIO.FALLING, callback=self.TakePicture, bouncetime=200)
        GPIO.add_event_detect(button2, GPIO.FALLING, callback=self.Shutdown, bouncetime=200)
        GPIO.add_event_detect(button4, GPIO.FALLING, callback=self.switch_cam, bouncetime=200)

        size = width, height = 160, 128
        screen = pygame.display.set_mode(size)
        # Running = True
        Exif = exif()
        flag = True
        # flag_switch = True
        try:
            while self.Running:
                while flag:
                    image = self.cam.get_image()
                    image2 = self.cam2.get_image()
                    if (self.flag_switch):
                        image_s = pygame.transform.scale(image, (160, 128))
                    else:
                        image_s = pygame.transform.scale(image2, (160, 128))
                    screen.blit(image_s, (0, 0))
                    pygame.draw.rect(screen, (0, 255, 0), [20, 32, 120, 64], 3)
                    pygame.display.update()

                if (~flag):
                    print('Taking a picture')
                    PictureName = '/home/pi/my_pictures/' + str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')) + '.jpg'
                    PictureName2 = '/home/pi/my_pictures_pc2/' + PictureName[21:-1] + 'g'
                    img = self.cam.get_image()
                    img2 = self.cam2.get_image()

                    pygame.image.save(img, PictureName)
                    pygame.image.save(img2, PictureName2)

                    im = Image.open(PictureName)
                    im2 = Image.open(PictureName2)

                    im_crop = im.crop((80, 120, 560, 360))
                    im_crop2 = im2.crop((80, 120, 560, 360))
                    im_crop.save(PictureName[0:20] + '_en/' + PictureName[21:40])
                    im_crop2.save(PictureName2[0:24] + '_en/' + PictureName[-19:])
                    Exif.star()

                    while input_value == False:
                        input_value = GPIO.input(button1)
                    if self.num % 2 == 0:
                        img_resize = pygame.transform.scale(img, (160, 128))
                    else:
                        img_resize = pygame.transform.scale(img2, (160, 128))

                    screen.blit(img_resize, (0, 0))
                    pygame.display.update()

                    # write txt file
                    TxtName = '/home/pi/Txt/' + str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')) + '.txt'
                    cmd_txt = 'sudo touch ' + TxtName
                    os.system(cmd_txt)
                    flag = True

        except KeyboardInterrupt:
            print('\nEnd program')
        except:
            print('\nUnkonwn Error')
        finally:
            GPIO.cleanup()
            # cambool = self.cam.query_image()
            # if (cambool):
            #     self.cam.stop()

if __name__ == "__main__":
    doubleCam = double_cam()
    doubleCam.run_cam()