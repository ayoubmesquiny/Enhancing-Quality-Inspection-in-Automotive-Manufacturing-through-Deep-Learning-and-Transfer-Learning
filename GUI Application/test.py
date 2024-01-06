import cv2
import tensorflow as tf
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
import os
from pyueye import ueye
import numpy as np

#===========================================================================#
#                                                                           #
#  Copyright (C) 2006 - 2018                                                #
#  IDS Imaging Development Systems GmbH                                     #
#  Dimbacher Str. 6-8                                                       #
#  D-74182 Obersulm, Germany                                                #
#                                                                           #
#  The information in this document is subject to change without notice     #
#  and should not be construed as a commitment by IDS Imaging Development   #
#  Systems GmbH. IDS Imaging Development Systems GmbH does not assume any   #
#  responsibility for any errors that may appear in this document.          #
#                                                                           #
#  This document, or source code, is provided solely as an example          #
#  of how to utilize IDS software libraries in a sample application.        #
#  IDS Imaging Development Systems GmbH does not assume any responsibility  #
#  for the use or reliability of any portion of this document or the        #
#  described software.                                                      #
#                                                                           #
#  General permission to copy or modify, but not for profit, is hereby      #
#  granted, provided that the above copyright notice is included and        #
#  reference made to the fact that reproduction privileges were granted     #
#  by IDS Imaging Development Systems GmbH.                                 #
#                                                                           #
#  IDS Imaging Development Systems GmbH cannot assume any responsibility    #
#  for the use or misuse of any portion of this software for other than     #
#  its intended diagnostic purpose in calibrating and testing IDS           #
#  manufactured cameras and software.                                       #
#                                                                           #
#===========================================================================#

# Developer Note: I tried to let it as simple as possible.
# Therefore there are no functions asking for the newest driver software or freeing memory beforehand, etc.
# The sole purpose of this program is to show one of the simplest ways to interact with an IDS camera via the uEye API.
# (XS cameras are not supported)
#---------------------------------------------------------------------------------------------------------------------------------------

#Libraries
from pyueye import ueye
import numpy as np
import cv2
import sys

#---------------------------------------------------------------------------------------------------------------------------------------

#Variables
hCam = ueye.HIDS(0)             #0: first available camera;  1-254: The camera with the specified camera ID
sInfo = ueye.SENSORINFO()
cInfo = ueye.CAMINFO()
pcImageMemory = ueye.c_mem_p()
MemID = ueye.int()
rectAOI = ueye.IS_RECT()
pitch = ueye.INT()
nBitsPerPixel = ueye.INT(24)    #24: bits per pixel for color mode; take 8 bits per pixel for monochrome
channels = 3                    #3: channels for color mode(RGB); take 1 channel for monochrome
m_nColorMode = ueye.INT()       # Y8/RGB16/RGB24/REG32
bytes_per_pixel = int(nBitsPerPixel / 8)
#---------------------------------------------------------------------------------------------------------------------------------------
print("START")
print()


# Starts the driver and establishes the connection to the camera
nRet = ueye.is_InitCamera(hCam, None)
if nRet != ueye.IS_SUCCESS:
    print("is_InitCamera ERROR")

# Reads out the data hard-coded in the non-volatile camera memory and writes it to the data structure that cInfo points to
nRet = ueye.is_GetCameraInfo(hCam, cInfo)
if nRet != ueye.IS_SUCCESS:
    print("is_GetCameraInfo ERROR")

# You can query additional information about the sensor type used in the camera
nRet = ueye.is_GetSensorInfo(hCam, sInfo)
if nRet != ueye.IS_SUCCESS:
    print("is_GetSensorInfo ERROR")

nRet = ueye.is_ResetToDefault( hCam)
if nRet != ueye.IS_SUCCESS:
    print("is_ResetToDefault ERROR")

# Set display mode to DIB
nRet = ueye.is_SetDisplayMode(hCam, ueye.IS_SET_DM_DIB)

# Set the right color mode
if int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
    # setup the color depth to the current windows setting
    ueye.is_GetColorDepth(hCam, nBitsPerPixel, m_nColorMode)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("IS_COLORMODE_BAYER: ", )
    print("\tm_nColorMode: \t\t", m_nColorMode)
    print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
    print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
    print()

elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
    # for color camera models use RGB32 mode
    m_nColorMode = ueye.IS_CM_BGRA8_PACKED
    nBitsPerPixel = ueye.INT(32)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("IS_COLORMODE_CBYCRY: ", )
    print("\tm_nColorMode: \t\t", m_nColorMode)
    print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
    print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
    print()

elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
    # for color camera models use RGB32 mode
    m_nColorMode = ueye.IS_CM_MONO8
    nBitsPerPixel = ueye.INT(8)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("IS_COLORMODE_MONOCHROME: ", )
    print("\tm_nColorMode: \t\t", m_nColorMode)
    print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
    print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
    print()

else:
    # for monochrome camera models use Y8 mode
    m_nColorMode = ueye.IS_CM_MONO8
    nBitsPerPixel = ueye.INT(8)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("else")

# Can be used to set the size and position of an "area of interest"(AOI) within an image
nRet = ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_GET_AOI, rectAOI, ueye.sizeof(rectAOI))
if nRet != ueye.IS_SUCCESS:
    print("is_AOI ERROR")

width = rectAOI.s32Width
height = rectAOI.s32Height

# Prints out some information about the camera and the sensor
print("Camera model:\t\t", sInfo.strSensorName.decode('utf-8'))
print("Camera serial no.:\t", cInfo.SerNo.decode('utf-8'))
print("Maximum image width:\t", width)
print("Maximum image height:\t", height)
print()

#---------------------------------------------------------------------------------------------------------------------------------------

# Allocates an image memory for an image having its dimensions defined by width and height and its color depth defined by nBitsPerPixel
nRet = ueye.is_AllocImageMem(hCam, width, height, nBitsPerPixel, pcImageMemory, MemID)
if nRet != ueye.IS_SUCCESS:
    print("is_AllocImageMem ERROR")
else:
    # Makes the specified image memory the active memory
    nRet = ueye.is_SetImageMem(hCam, pcImageMemory, MemID)
    if nRet != ueye.IS_SUCCESS:
        print("is_SetImageMem ERROR")
    else:
        # Set the desired color mode
        nRet = ueye.is_SetColorMode(hCam, m_nColorMode)



# Activates the camera's live video mode (free run mode)
nRet = ueye.is_CaptureVideo(hCam, ueye.IS_DONT_WAIT)
if nRet != ueye.IS_SUCCESS:
    print("is_CaptureVideo ERROR")

# Enables the queue mode for existing image memory sequences
nRet = ueye.is_InquireImageMem(hCam, pcImageMemory, MemID, width, height, nBitsPerPixel, pitch)
if nRet != ueye.IS_SUCCESS:
    print("is_InquireImageMem ERROR")
else:
    print("Press q to leave the programm")

#---------------------------------------------------------------------------------------------------------------------------------------



class VideoCaptureApp(QMainWindow):
    def __init__(self):
        super(VideoCaptureApp, self).__init__()

        self.showMaximized()
        self.setWindowIcon(QIcon('img/learLogo.png'))
        self.setWindowTitle("Lear - CCSC: Crimp Cross Section Classifier")

        # Create widgets
        self.video_label = QtWidgets.QLabel(self)
        self.record_button = QtWidgets.QPushButton(self)
        self.record_button.setText("Inspect")  # Add text to the button
        self.record_button.setStyleSheet("""
                                        QPushButton {
                                            background-color: red; /* Green */
                                            border: none;
                                            color: white;
                                            padding: 15px 32px;
                                            text-align: center;
                                            text-decoration: none;
                                            display: inline-block;
                                            font-size: 16px;
                                            margin: 4px 2px;
                                            transition-duration: 1.0s;
                                            border-radius:18px;
                                            width:100px;
                                            
                                        }

                                        QPushButton:hover {
                                            background-color: white;
                                            color: red;
                                            border: 1px solid red;
                                            cursor: pointer;
                                        }
                                    """)

        # Create a layout and add widgets to it
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_label)
        layout.addWidget(self.record_button)

        # Set the layout for the central widget
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.model = self.load_model()  # Initialize model in the constructor

        self.record_button.clicked.connect(self.save_frame)

    @staticmethod
    def load_model():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, 'model/ResNet50V2.h5')
        return tf.keras.models.load_model(model_path)

    @staticmethod
    def predict(image, model):
        # Preprocess the image
        resized_image = image.resize((224, 224))
        normalized_image = tf.keras.preprocessing.image.img_to_array(resized_image) / 255.0
        input_image = tf.expand_dims(normalized_image, axis=0)

        # Make the prediction
        prediction = model.predict(input_image)
        predicted_class_index = tf.argmax(prediction[0]).numpy()
        predicted_class_probability = prediction[0][predicted_class_index]

        return predicted_class_index, predicted_class_probability

    def update_frame(self):
        # In order to display the image in an OpenCV window we need to...
        # ...extract the data of our image memory
        array = ueye.get_data(pcImageMemory, width, height, nBitsPerPixel, pitch, copy=False)

        # ...reshape it in a numpy array...
        frame = np.reshape(array, (height.value, width.value, bytes_per_pixel))
        self.capture = frame

        frame = self.capture
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.video_label.width(), self.video_label.height())
        self.video_label.setPixmap(QPixmap.fromImage(p))

    def save_frame(self):
        class_labels = ['Non-Defective', 'Defective']
        frame = self.capture
        cv2.imwrite("derniere_frame.jpg", frame)
        image = Image.open("derniere_frame.jpg")
        predicted_class_index, predicted_class_probability = self.predict(image, self.model)
        # Apply threshold
        threshold = 0.5
        if predicted_class_probability >= threshold:
            predicted_class = class_labels[predicted_class_index]
            self.inspect_and_show_message("Prediction: Non-Defective",True)
            self.inspect_and_create_folders()
            file_path = os.path.abspath('Inspect/OK/ok.txt')
            with open(file_path, 'r') as file:
                data = file.read()
            cv2.imwrite(f"Inspect/OK/OK{data}.jpg", frame)
            data=str(int(data)+1)
            with open(file_path, 'w') as file:
                file.write(data)
        else:
            predicted_class = 'Defective'
            self.inspect_and_create_folders()
            file_path = os.path.abspath('Inspect/NOK/nok.txt')
            with open(file_path, 'r') as file:
                data = file.read()
            cv2.imwrite(f"Inspect/NOK/NOK{data}.jpg", frame)
            data=str(int(data)+1)
            with open(file_path, 'w') as file:
                file.write(data)
            self.inspect_and_show_message("Prediction: Defective",False)


    def inspect_and_show_message(self,message,type):
        type = True  
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Inspection Result")

        if type:
            msg_box.setText(message)
            msg_box.setIcon(QMessageBox.Information)
        else:
            msg_box.setText(message)
            msg_box.setIcon(QMessageBox.Warning)

        msg_box.exec_()

    def inspect_and_create_folders(self):
        inspect_folder = "Inspect"
        ok_folder = os.path.join(inspect_folder, "OK")
        nok_folder = os.path.join(inspect_folder, "NOK")

        if not os.path.exists(inspect_folder):
            os.makedirs(inspect_folder)
            os.makedirs(ok_folder)
            os.makedirs(nok_folder)
            print("Folders created: Inspect, OK, NOK")
            with open(os.path.join(ok_folder, "ok.txt"), 'w') as ok_file:
                ok_file.write("1")

            with open(os.path.join(nok_folder, "nok.txt"), 'w') as nok_file:
                nok_file.write("1")
        else:
            print("Folders already exist: Inspect, OK, NOK")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = VideoCaptureApp()
    window.show()
    sys.exit(app.exec_())
