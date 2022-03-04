import cv2
import os
import image_similarity_measures
from sys import argv
from image_similarity_measures.quality_metrics import rmse, ssim, sre
from tqdm import tqdm

import glob
import re
import pandas as pd

def calc_closest_val(dict, checkMax):
    result = ['','','','','']
    values = list(dict.values())
    if (checkMax):
        sorted_list = sorted(values, reverse=True)
        
    else:
        sorted_list = sorted(values)

    for key, value in dict.items():
        if (value in sorted_list[:5]):
            index = sorted_list[:5].index(value)
            result[index] = key.split('/')[-1]
    return result, sorted_list[:5]

images = glob.glob('/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/memes/*')

### for additional ###
df = pd.read_csv('/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/csv_files/edited_scraped_memes.csv')
prev_filenames = df['filename'].unique().tolist()
target_images = []
for filename in prev_filenames:
    target_images.append("/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/memes/" + filename)
df2 = pd.read_csv('/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/csv_files/scraped_memes.csv')
prev_filenames2_tmp = df2['filename'].unique().tolist()
prev_filenames2 = []
for filename in prev_filenames2_tmp:
    prev_filenames2.append("/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/memes/" + filename)
orig_images = list(set(images) ^ set(prev_filenames2))
images = orig_images
###    ###

for i, image in enumerate(tqdm(images)):
    test_img = cv2.imread(image)
    ssim_measures = {}
    rmse_measures = {}
    sre_measures = {}

    scale_percent = 100 # percent of original img size
    width = int(test_img.shape[1] * scale_percent / 100)
    height = int(test_img.shape[0] * scale_percent / 100)
    dim = (width, height)
    #for file in images[i+1:]:
    for file in target_images:
        img_path = file
        data_img = cv2.imread(img_path)
        resized_img = cv2.resize(data_img, dim, interpolation = cv2.INTER_AREA)
        ssim_measures[img_path] = ssim(test_img, resized_img)
        rmse_measures[img_path] = rmse(test_img, resized_img)
    ssim_result, ssim_value = calc_closest_val(ssim_measures, True)
    rmse_result, rmse_value = calc_closest_val(rmse_measures, False)
    if ssim_value[0] > 0.92 or rmse_value[0] < 0.011:
        print(image)
        print(ssim_result)
        print(rmse_result)
        print(ssim_value)
        print(rmse_value)
        print("")
