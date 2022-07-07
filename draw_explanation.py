import cv2
import time

def add_exp(img, anno_img_path, text):
    now = time.time()
    # 画像をとってくる

    anno_im = img.copy()

    # 青色背景の表示
    blu1 = (0, 0)
    blu2 = (1360, 200)
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
    ja_im = cv2.imread(anno_img_path)
    ja_im = cv2.resize(ja_im, dsize=(160, 160))
    mat_im[20:180, 1140:1300] = ja_im

    # 文字の表示
    cv2.putText(mat_im, text, (0, 100), 0, 2, (0,0,0), 5, cv2.LINE_AA)

    # cv2.imwrite('test2.png', mat_im)
    
    elapsed_time = time.time() - now
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    # 該当する説明文をとってくる
    return mat_im
def main():
    img_path = "runs/detect/exp5/00001.png"
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    add_exp(img, 'ja_img.png', "good luck for your drive!")
    pass

if __name__ == "__main__":
    main()