"""
imgflip.com scraper
This script scrapes memes from a category on imgflip.com
(e.g. https://imgflip.com/meme/Bird-Box). As an example,
to scrape the first 10 pages of Bird Box memes run:
python imgflip_scraper.py --source https://imgflip.com/meme/Bird-Box --pages 10
The program outputs the memes as a JSON file with the following format:
{
    "name": "Bird Box",
    "memes": [{
        "url": "i.imgflip.com/40y9fr.jpg",
        "text": "YOU CAN'T GET CORONA; IF YOU CAN'T SEE IT"
    }, ...]
}
"""

import time
import json
import argparse
import requests
import pandas as pd
import shutil
from bs4 import BeautifulSoup
from tqdm import tqdm


def scrape_memes(source_list, n_captions):
    n_pages = n_captions // 14
    column_names = ['url', 'filename', 'uppercaption', 'lowercaption', 'views', 'upvote']
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
        #img_url = img_body.find("a", {"class": "meme-link"}).find("img")['src']
        #print(img_url)
        img_file_name = source.split("/")[-1] + '.' + img_url.split('/')[-1].split('.')[-1]
        #print(img_file_name)
        img = requests.get(img_url, stream=True)
        #print(img.status_code)
        savefile = "/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/memes/" + img_file_name
        with open(savefile,'wb') as out_file:
            shutil.copyfileobj(img.raw, out_file)
        del img 

        caption_counter = 0

        for i in range(1, n_pages + 1):
            response = requests.get(f"{source}?page={i}")
            body = BeautifulSoup(response.text, 'html.parser')

            if response.status_code != 200:
                # Something went wrong (e.g. page limit)
                break

            memes = body.findAll("div", {"class": "base-unit clearfix"})
            #print(memes)
            #print(i)

            for meme in memes:
                if "not-safe-for-work images" in str(meme):
                    # NSFW memes are available only to logged in users
                    continue
                
                if meme.find("img", {"class": "base-img"}) == None:
                    continue
                meme_text = meme.find("img", {"class": "base-img"})["alt"]
                meme_text = meme_text.split("|")[1].strip()
                if "\n" in meme_text:
                    meme_text = meme_text.replace("\n", " ")
                rows = meme_text.split(";")
                if len(rows) != 2:
                    # select ones with upper and lower caption
                    continue
                meme_page_url = "https://imgflip.com" + meme.find("a", {"class": "base-img-link"})['href']
                meme_page_response = requests.get(meme_page_url)
                meme_page_body = BeautifulSoup(meme_page_response.text, 'html.parser')
                added_imgs = len(meme_page_body.findAll("div", {"class": "img-added-imgs-msg"}))
                if added_imgs != 0:
                    # select only memes without added images
                    continue

                uppercaption = str(rows[0]).lower()
                lowercaption = str(rows[1][1:]).lower()
                meme_url = "https://" + meme.find("img", {"class": "base-img"})["src"][2:]
                meme_view_votes = meme.find("div", {"class": "base-view-count"}).text.split(" ")
                if len(meme_view_votes) == 0:
                    views = 0
                    upvotes = 0
                elif len(meme_view_votes) > 0:
                    if "," in meme_view_votes[0]:
                        views = int(meme_view_votes[0].replace(",",""))
                    else:
                        views = int(meme_view_votes[0])
                    if len(meme_view_votes) > 2 and (meme_view_votes[3] == "upvote" or meme_view_votes[3] == "upvotes"):
                        if "," in meme_view_votes[2]:
                            upvotes = int(meme_view_votes[2].replace(",",""))
                        else:
                            upvotes = int(meme_view_votes[2])
                    else:
                        upvotes = 0   

                d = {'url': meme_url, 'filename': img_file_name, 'uppercaption': uppercaption, 'lowercaption': lowercaption, 'views': views, 'upvote': upvotes}
                row = pd.DataFrame(d.values(), index=d.keys()).T 
                df = pd.concat([df, row])
                caption_counter += 1
                time.sleep(0.5)
            if caption_counter > 300:
                break
        df.to_csv('scraped_memes.csv', index=False)





if __name__ == "__main__":
    #source_list = ["https://imgflip.com/meme/Joseph-Ducreux"]
    
    with open('source_list.txt') as f:
        contents = f.read()
    source_list = contents.split('\n')
    
    #source_list = list(set(source_list))
    print(len(source_list))
    scrape_memes(source_list=source_list, n_captions=2000)

