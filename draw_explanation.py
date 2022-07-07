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


def add_exp(img, anno_img_paths, texts):
    now = time.time()
    # 画像をとってくる

    anno_im = img.copy()
    h, w, _ = anno_im.shape

    # 青色背景の表示
    h_background = h // 5
    blu1 = (0, 0)
    blu2 = (w, h_background)
    blue = (255, 200, 80)
    cv2.rectangle(
        anno_im,
        blu1,
        blu2,
        blue,
        thickness=-1,
        lineType=cv2.LINE_AA,
        shift=0)

    # 青色背景を合成
    mat_im = cv2.addWeighted(anno_im, 0.4, img, 0.6, 0)

    # print(anno_im.shape)  # (360, 480, 3)
    sign_size = h_background // 3 * 2
    img_pad = h // 72
    font_path = "./GenShinGothic-Bold.ttf"
    text_height = h // 18
    text_pad = h // 72

    # 検出したbboxの数だけ
    for idx, (anno_img_path, text) in enumerate(zip(anno_img_paths, texts)):
        # 該当する画像の描画
        ja_im = cv2.imread(anno_img_path)
        ja_im = cv2.resize(ja_im, dsize=(sign_size, sign_size))
        mat_im[img_pad:img_pad+sign_size, w-(sign_size+img_pad)*(idx+1):w-img_pad-(sign_size+img_pad)*idx] = ja_im

        # 文字の描画
        mat_im = cv2_putText_2(mat_im, text, (text_pad, (idx + 1) * (text_pad + text_height)), font_path, text_height, (0, 0, 0))

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
