import re
from os.path import dirname, join
import difflib
import yaml
import random
try:
    import hjson as json
except:
    import json

curpath = dirname(__file__) #当前路径

config_path = join(curpath,"config.yaml")
f = open(config_path, 'r', encoding='utf-8')
config = yaml.safe_load(f)#读取配置文件

with open(join(curpath, './magicbooks/magic.json'),encoding="utf-8") as f: #初始化法典
    magic_data = json.load(f)
with open(join(curpath, './magicbooks/magic_pure.json'),encoding="utf-8") as f: #初始化法典(纯净版)
    magic_data_pure = json.load(f)
magic_data_title = []
for i in magic_data:
    magic_data_title.append(i) #初始化法典目录

with open(join(curpath, './magicbooks/magic_dark.json'),encoding="utf-8") as f: #初始化法典(黑暗版)
    magic_data_dark = json.load(f)
magic_data_dark_title = []
for i in magic_data_dark:
    magic_data_dark_title.append(i) #初始化黑暗法典目录


async def get_magic_book_(msg):
    error_msg = ""
    error_msg,magic_msg_tag,magic_msg_ntag,magic_msg_scale = await mix_magic_(msg) #获取魔法书
    if error_msg != "":
        return None,error_msg,None
    result_msg = magic_msg_tag +"&ntags="+ magic_msg_ntag +"&shape=Landscape"+"&scale=" + magic_msg_scale
    node_msg = f'正面tags:{magic_msg_tag}\n负面tags:{magic_msg_ntag}\nscale:{magic_msg_scale}'
    node_data ={
        "type": "node",
        "data": {
            "name": '图书管理员小冰',
            "uin": '2854196306',
            "content": node_msg
        }
        }
    return result_msg,error_msg,node_data

async def mix_magic_(msg):
    error_msg = ""
    magic_msg = ""
    magic_msg_pure = ""
    magic_id_list = re.split('\\s+',msg)
    for i in magic_id_list:
        if i in magic_data_title:
            magic_msg += f'{magic_data[i]["tags"]},'
            magic_msg_pure += f'{magic_data_pure[i]["tags"]},'
            magic_msg_ntag = magic_data[i]["ntags"]
            magic_msg_scale = magic_data[i]["scale"]
    if not magic_msg:
        error_msg = "发动魔法失败"
        return error_msg,None,None,None
    magic_list = re.split(',',magic_msg)
    magic_list_pure = re.split(',',magic_msg_pure)
    for i in range(len(magic_list)-1,-1,-1):
        j=i-1
        if i == 0:
            break
        for j in range(j,-1,-1):
            seq=  difflib.SequenceMatcher(lambda x: x ==" ",magic_list_pure[i],magic_list_pure[j])
            if seq.ratio()> config['max_ratio']: #相似度大于0.8则删除
                magic_list[j] = ""
                magic_list_pure[j] = ""
    while "" in magic_list:
        magic_list.remove("")
    magic_msg_tag = ",".join(magic_list)
    if "咏唱" in msg:
        dark = random.choice(magic_data_dark_title)
        magic_msg_tag += f'{magic_data_dark[dark]["tags"]},'
        magic_msg_ntag = magic_data_dark[dark]["ntags"]
    return error_msg,magic_msg_tag,magic_msg_ntag,magic_msg_scale
    #融合魔法以最后融合的魔法作为基准!!!