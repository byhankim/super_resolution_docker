import tensorflow as tf
import tensorflow_datasets as tfds 

from skimage import data
import cv2
import numpy as np
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
from tensorflow.keras import Input, Model


# crop function
def crop(image, left_top, x=50, y=100):
    return image[left_top[0]:(left_top[0]+x),
    left_top[1]:(left_top[1])+y, :]


def preprocessing(lr, hr):
    hr = tf.cast(hr, tf.float32) /255.
        
    # 이미지의 크기가 크므로 (96,96,3) 크기로 임의 영역을 잘라내어 사용합니다.
    hr_patch = tf.image.random_crop(hr, size=[96,96,3])
        
    # 잘라낸 고해상도 이미지의 가로, 세로 픽셀 수를 1/4배로 줄입니다
    # 이렇게 만든 저해상도 이미지를 SRGAN의 입력으로 사용합니다.
    lr_patch = tf.image.resize(hr_patch, [96//4, 96//4], "bicubic")
    return lr_patch, hr_patch

def model_load():
    model_file = load_model("srgan_G.h5")
    srgan = tf.keras.models.load_model(model_file)


def apply_srgan(image):
    image = tf.cast(image[np.newaxis, ...], tf.float32)
    sr = srgan.predict(image)
    sr = tf.clip_by_value(sr, 0, 255)
    sr = tf.round(sr)
    sr = tf.cast(sr, tf.uint8)
    return np.array(sr)[0]




# =====================================================================================
#
#       SRGAN project 1-2
#           bicubic vs srgan
#
# =====================================================================================
def run_srgan():
    lr = Image.open('aish.jpg')
    lr = np.array(asarray(lr))

    # plt.imshow(lr)

    # 2
    srgan_hr = apply_srgan(lr)

    # 3
    bicubic_hr = cv2.resize(
        lr,
        (lr.shape[1]*4, lr.shape[0]*4),
        interpolation=cv2.INTER_CUBIC
    )
    print(lr.shape, srgan_hr.shape, bicubic_hr.shape)


    # 4
    imgs = [bicubic_hr, srgan_hr]
    titles = ["Bicubic", "SRGAN"]

    # 잘라낼 부분의 왼쪽 상단 좌표를 지정합니다.
    left_top = (650, 100) 

    # crop 함수 내의 세번째 네번째 인자를 수정해 이미지 크기를 조절합니다.
    crop_images = [crop(i, left_top, 250, 250) for i in imgs] 
    titles = ["Bicubic", "SRGAN"]

    psnr = [round(peak_signal_noise_ratio(crop_images[-1], i), 2) for i in crop_images]
    ssim = [round(structural_similarity(crop_images[-1], i, multichannel=True), 2) for i in crop_images]

    plt.figure(figsize=(20,20)) # 이미지 크기를 조절할 수 있습니다.
    for i in range(2):
        plt.subplot(1, 2, i+1)
        # crop 함수 내의 세번째 네번째 인자를 수정해 이미지 크기를 조절합니다.
        plt.imshow(crop(imgs[i], left_top, 350, 350))
        plt.title(titles[i] + f" [{psnr[i]}/{ssim[i]}]", fontsize=30)