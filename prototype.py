from re import U
import streamlit as st
from PIL import Image
import cv2
import numpy as np
import time
import datetime
import os
import glob
from datetime import datetime, date, time
import detect
st.write("test")
def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image
def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image

def input():
    uploaded_file=st.file_uploader("choose file", type=['jpg', 'png', 'mp4', 'jpeg'])
    if uploaded_file is not None:
        if uploaded_file.type !=  'mp4':
            st.write(uploaded_file.type)
            image=Image.open(uploaded_file)
            img_array = np.array(image)
            cvimg=pil2cv(img_array)
            cvimg, s =detect.do(cvimg)
            st.image(cvimg,caption = s.split()[-2],use_column_width = True)
        else :
            main()
            # -*- coding: utf-8 -*-



PATH='/home/mars/pWork/DATA/'

def disp(device):
    cap = cv2.VideoCapture(device)
    image_loc = st.empty()
    while cap.isOpened:
        ret, img = cap.read()
        if ret:
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            image_loc.image(img)
        else:
            break

    cap.release()
    st.button('Replay')

def main():
    st.header("流星観測データの表示")
    date=st.date_input('Select date')
    path=PATH+date.strftime("%Y%m%d")
    #st.write(path)
    if os.path.exists(path):
        files=glob.glob(path+'/*avi')
        option = st.selectbox('Select file:',files)
        disp(option)
    else:
        st.write('No data exists!')

            
input()
