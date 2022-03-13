import time
import json
import argparse
import requests
import pandas as pd
import shutil
from bs4 import BeautifulSoup
from tqdm import tqdm

def scrape_image_url(source_list):
    column_names = ['filename', 'img_url']
    df = pd.DataFrame(columns=column_names)
    for source in tqdm(source_list):
        print(source)
        meme_name = source.split("/")[-1].replace("-", " ")
        img_response = requests.get(f"{source}?page=0")
        img_body = BeautifulSoup(img_response.text, 'html.parser')
        if "i.imgflip.com" in img_body.find("a", {"class": "meme-link"}).find("img")['src']:
            img_url = "https:" + img_body.find("a", {"class": "meme-link"}).find("img")['src']
        else:
            img_url = "https://imgflip.com" + img_body.find("a", {"class": "meme-link"}).find("img")['src']
        img_file_name = source.split("/")[-1] + '.' + img_url.split('/')[-1].split('.')[-1]
        d = {'filename' : img_file_name, 'img_url' : img_url}
        row = pd.DataFrame(d.values(), index=d.keys()).T 
        df = pd.concat([df, row])
        time.sleep(0.5)
    
        df.to_csv('csv_files/scraped_imgurl.csv', index=False)

if __name__ == '__main__':
    with open('source_list.txt') as f:
        contents = f.read()
    source_list = contents.split('\n')
    scrape_image_url(source_list)