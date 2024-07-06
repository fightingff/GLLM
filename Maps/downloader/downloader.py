import requests
import random
import math

URL = "http://mt{id}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}&s=Gali&t=2000"

def download_tile(x, y, z):
    url = URL.format(id=random.randint(0,3), x=x, y=y, z=z)
    print(url)
    response = requests.get(url)
    img = response.content
    return img

TILE_SIZE = 256

# Convert longitude, latitude to web mercator
def convert_to_web_mercator(longitude, latitude, zoom=17):
    mercator = -math.log(math.tan((0.25 + latitude / 360) * math.pi))
    x = TILE_SIZE * (longitude / 360 + 0.5)
    y = TILE_SIZE / 2 * (1 +  mercator / math.pi)
    scale = 2 ** zoom / TILE_SIZE
    x = int(x * scale)
    y = int(y * scale)
    return x, y, int(zoom)

if __name__ == "__main__":
    x, y, z = input("Enter x, y, z: ").split(',')
    x, y, z = float(x), float(y), float(z)
    img = download_tile(*convert_to_web_mercator(x, y, z))
    with open("tile.png", "wb") as f:
        f.write(img)