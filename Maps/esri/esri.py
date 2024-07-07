import requests
import random
import math
import matplotlib.pyplot as plt
from PIL import Image


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


# 传入经纬度，下载瓦片
def download_tile(path, lon, lat, year, zoom=17):
    xtile, ytile = lat_lon_to_tile(lon, lat, zoom)
    url = construct_url(xtile, ytile, zoom, timestamp[year])
    
    # 选择时间最邻近的瓦片
    

    # 将邻近的9个瓦片下载下来
    id = 0
    for j in range(-1, 2):
        for i in range (-1, 2):
            url = construct_url(xtile + i, ytile + j, zoom, timestamp[year])
            img = requests.get(url).content
            with open(f"{path}/tile{id}.png", "wb") as f:
                f.write(img)
            id += 1

def test():
    year = 2019
    lon, lat, zoom = input("Enter lon, lat, zoom: ").split(',')
    lon, lat, zoom = float(lon), float(lat), int(zoom)
    xtile, ytile = lat_lon_to_tile(lon, lat, zoom)
    id = 0
    for j in range(-1, 2):
        for i in range (-1, 2):
            url = construct_url(xtile + i, ytile + j, zoom)
            print(url)
            img = requests.get(url).content
            with open(f"tile{id}.png", "wb") as f:
                f.write(img)
            id += 1

def show_map(path):
    plt.figure(figsize=(9, 9))
    # plt.title(f"{year},    longitude: {lon}, latitude: {lat}")
    plt.axis('off')
    for i in range(9):
        img = f"{path}tile{i}.png"
        print(img)
        img = Image.open(img)
        plt.subplot(3, 3, i + 1)
        plt.axis('off')
        plt.imshow(img)
    
    plt.subplots_adjust(wspace=0.02, hspace=0.02)
    plt.show()

if __name__ == "__main__":
    # test()
    show_map('data/0/')
