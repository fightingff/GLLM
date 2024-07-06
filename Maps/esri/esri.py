import requests
import random
import math
import matplotlib.pyplot as plt
from PIL import Image

def lat_lon_to_tile(lon, lat, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def construct_url(xtile, ytile, zoom, time='11351'):
    base_url = 'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile'
    url = f"{base_url}/{time}/{int(zoom)}/{ytile}/{xtile}"
    return url

if __name__ == "__main__":
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

    for i in range(id):
        img = f"tile{i}.png"
        print(img)
        img = Image.open(img)
        plt.subplot(3, 3, i + 1)
        plt.axis('off')
        plt.imshow(img)
    
    plt.subplots_adjust(wspace=0, hspace=0.02)
    plt.show()

