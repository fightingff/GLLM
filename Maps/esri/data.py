import pandas as pd
from esri import download_tile
from pathlib import Path

data = pd.read_csv('india_infant_mort.csv')

# 只处理infant_mort不为0且年份大于等于2010的数据
data = data[(data['infant_mort'] != 0) & (data['year'] >= 2010) ]

# 为方便处理，将数据按照年份排序
data = data.sort_values(by='year')

# 创建data文件夹
base_path = Path('data/')

with open('item.csv', 'w') as f:
    f.write('item,lon,lat,year,infant_mort\n')
    item = 0
    for i, row in data.iterrows():
        lon, lat, year = row['lon'], row['lat'], row['year']
        # 确保每个item对应的文件夹存在
        item_path = base_path / str(item)
        item_path.mkdir(parents=True, exist_ok=True)
        
        download_tile(str(item_path), lon, lat, year)
        f.write(f"{item},{lon},{lat},{year},{row['infant_mort']}\n")
        item += 1
        print(f"Downloaded {item}")