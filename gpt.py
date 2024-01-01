from openai import OpenAI
from time import sleep
from Getmap import GetImage
client = OpenAI()


cordinates = []
index = 0
cities = ["Beijing", "Shanghai", "Chongqing", "Tianjin", "Guangzhou", "Shenzhen", "Chengdu", "Nanjing", "Wuhan", "Xi'an", "Hangzhou", "Shenyang", "Harbin", "Jinan", "Zhengzhou", "Changsha", "Kunming", "Fuzhou", "Nanchang", "Hefei", "Urumqi", "Lanzhou", "Xining", "Yinchuan", "Taiyuan", "Changchun", "Haikou", "Nanning", "Guiyang", "Shijiazhuang", "Suzhou", "Qingdao", "Dalian", "Wuxi", "Xiamen", "Ningbo", "Foshan", "Dongguan", "Shantou", "Zhuhai", "Quanzhou", "Weifang", "Zibo", "Yantai", "Jinan", "Luoyang", "Kaifeng", "Xinxiang", "Anyang", "Zhumadian", "Nanyang", "Changde", "Yueyang", "Zhangjiajie", "Liuzhou", "Guilin", "Beihai", "Wuzhou", "Zunyi", "Anshun", "Kaili", "Lijiang", "Dali", "Baoshan", "Zhaotong", "Yuxi", "Hohhot", "Baotou", "Ordos", "Wuhai", "Hulunbuir", "Shenyang", "Dandong", "Anshan", "Fushun", "Benxi", "Yingkou", "Panjin", "Jinzhou", "Chaoyang", "Huludao", "Harbin", "Qiqihar", "Mudanjiang", "Jiamusi", "Daqing", "Yichun", "Jixi", "Hegang", "Shuangyashan", "Qitaihe", "Changchun", "Jilin", "Siping", "Liaoyuan", "Tonghua", "Baicheng", "Songyuan", "Yanbian", "Nancha", "Shulan"]
for city in cities:
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role":"system","content":"You are a map."},
        {"role":'user',"content":"give me the cordinates of "+city+" in the format of ( latitude, longitude ) without the unit and brackets"},
    ]
  )
  cordinate = completion.choices[0].message.content.split(" ")
  print(cordinate)
  latitude = float(cordinate[0][:-1])
  longitude = float(cordinate[1])
  cordinates.append([latitude, longitude])
  GetImage(latitude, longitude, path="image/"+str(index)+".png")
  index = index + 1

with open("cordinates.txt", "w") as f:
  f.write(str(cordinates))