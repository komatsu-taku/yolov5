import cv2
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def pil2cv(imgPIL):
    imgCV_BGR = np.array(imgPIL)[:, :, ::-1]
    return imgCV_BGR


def cv2pil(imgCV):
    imgCV_RGB = imgCV[:, :, ::-1]
    imgPIL = Image.fromarray(imgCV_RGB)
    return imgPIL


def cv2_putText_2(img, text, org, fontFace, fontScale, color):
    x, y = org
    b, g, r = color
    colorRGB = (r, g, b)
    imgPIL = cv2pil(img)
    draw = ImageDraw.Draw(imgPIL)
    fontPIL = ImageFont.truetype(font=fontFace, size=fontScale)
    w, h = draw.textsize(text, font = fontPIL)
    draw.text(xy=(x, y-h), text=text, fill=colorRGB, font=fontPIL)
    imgCV = pil2cv(imgPIL)
    return imgCV


def add_exp(img, anno_img_path, text):
    now = time.time()
    # 画像をとってくる

    anno_im = img.copy()
    y, x, _ = anno_im.shape

    # 青色背景の表示
    h_background = y // 5
    blu1 = (0, 0)
    blu2 = (x, h_background)
    blue = (255, 200, 80)
    cv2.rectangle(
        anno_im,
        blu1,
        blu2,
        blue,
        thickness=-1,
        lineType=cv2.LINE_AA,
        shift=0)

    mat_im = cv2.addWeighted(anno_im, 0.4, img, 0.6, 0)

    # 該当する画像の表示
    sign_size = h_background // 2
    ja_im = cv2.imread(anno_img_path)
    ja_im = cv2.resize(ja_im, dsize=(sign_size, sign_size))
    mat_im[0:sign_size, x-sign_size:x] = ja_im

    # 文字の表示
    font_path = "./GenShinGothic-Bold.ttf"
    mat_im = cv2_putText_2(mat_im, text, (0, h_background // 2), font_path, 20, (0,0,0))

    # cv2.imwrite('test2.png', mat_im)

    elapsed_time = time.time() - now
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    # 該当する説明文をとってくる
    return mat_im


def main():
    img_path = "runs/detect/exp5/00001.png"
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    add_exp(img, 'ja_img.png', "good luck for your drive!")


if __name__ == "__main__":
    main()
