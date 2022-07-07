import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2
from re import U
import streamlit as st
from PIL import Image
import cv2
import numpy as np
import time
import os
import glob
from datetime import datetime, date, time
import detect
import draw_explanation as dr
st.write("demo")
dir='sign/'
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
# st.title("My first Streamlit app")
# st.write("Hello, world")

table=[]
table.append(["no overtaking", '追い越し禁止', '9.png'])
table.append(["priority at next intersection",'一時優先', 'none.png'])
table.append(["priority road", '優先道路', '12.png'])
table.append(["give way", '前方優先道路・徐行', '13.png'])
table.append(["no traffic both ways", '車両通行禁止', '15.png'])
table.append(["no trucks", '3.5t以上の車両侵入禁止', '16.png'])
table.append(["danger", '危険', '18.png'])
table.append(["bend", '連続カーブあり', '21.png'])
table.append(["road narrows", '車線減少', '24.png'])

# for i in a:
#     table=np.append(table, np.array(i))
class VideoProcessor:
    def recv(self, frame):
        f=dir
        img = frame.to_ndarray(format="bgr24")
        img, s =detect.do(img)
        print('s',s)
        for i in table:
            if(i[1] in s):
                s=i[1]
                f+=i[2]
                break
        print('check')
        if f != dir:
            img=dr.add_exp(img, f, s)
        # st.image(cv2pil(img),caption = s.split()[-2],use_column_width = True)
        # img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(key="example", video_processor_factory=VideoProcessor)