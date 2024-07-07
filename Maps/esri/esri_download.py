"""
2024/7/7 cjl
"""
import io
import os
import requests
import random
import math
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

# 扒下来的瓦片的时间戳, 最早只能到2014年
timestamp = dict(
    {
        2023: '64776',
        2022: '47471',
        2021: '8432',
        2020: '20753',
        2019: '11351',
        2018: '2168',
        2017: '2168',
        2016: '6984',
        2015: '6984',
        2014: '23383',
        2013: '23383',
        2012: '23383',
        2011: '23383',
        2010: '23383',
        2009: '23383',
        2008: '23383',
        2007: '23383',
        2006: '23383',
        2005: '23383',
        2004: '23383',
        2003: '23383',
        2002: '23383',
    }
)

# 经纬度转瓦片坐标
def lat_lon_to_tile(lon, lat, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def construct_url(xtile, ytile, zoom, time):
    base_url = 'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile'
    url = f"{base_url}/{time}/{int(zoom)}/{ytile}/{xtile}"
    return url

# 传入经纬度，下载瓦片，并保存到指定路径
def download_tile(path, lon, lat, year, zoom=17):
    xtile, ytile = lat_lon_to_tile(lon, lat, zoom)
    images = []
    for j in range(-1, 2):
        for i in range(-1, 2):
            url = construct_url(xtile + i, ytile + j, zoom, timestamp[year])
            img = requests.get(url).content
            images.append(Image.open(io.BytesIO(img)))

    width, height = images[0].size
    new_image = Image.new('RGB', (width * 3, height * 3))
    index = 0
    for j in range(3):
        for i in range(3):
            new_image.paste(images[index], (i * width, j * height))
            index += 1
            
    new_image.save(path)

def download_tile_task(row):
    path = os.path.join('images', f"{row['cluster_id']}_{row['year']}.png")
    if os.path.exists(path):
        print(f"Tile for {row['cluster_id']} in {row['year']} already exists")
        return
    download_tile(path, row['lon'], row['lat'], row['year'])

    print(f"Downloaded tile for {row['cluster_id']} in {row['year']}")

if __name__ == "__main__":
    # 读取 india_infant_mort
    df = pd.read_csv('india_infant_mort.csv')

    os.makedirs('images', exist_ok=True)

    # 单线程
    # for index, row in df.iterrows():
    #     download_tile_task(row)

    # 多线程
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(download_tile_task, row) for index, row in df.iterrows()]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")