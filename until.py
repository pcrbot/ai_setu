from base64 import b64encode
from io import BytesIO
import re,json
from heapq import nsmallest
from hoshino import Service, priv, aiorequests
from PIL import Image, ImageDraw,ImageFont
from io import BytesIO
import base64
import time,calendar
import re
import os
import math
from os.path import dirname, join, exists
from . import youdao,db,easygradio
import ahocorasick
import uuid
import difflib
import asyncio
import yaml
try:
    import hjson as json
except:
    import json


curpath = dirname(__file__) #当前路径
save_image_path= join(curpath,'SaveImage')  # 保存图片路径
font_path = join(curpath,"weiheijun.ttf")  #字体文件路径
config_path = join(curpath,"config.yaml")
if not exists(save_image_path):
    os.mkdir(save_image_path) #创建img保存目录


f = open(config_path, 'r', encoding='utf-8')
config = yaml.safe_load(f)#读取配置文件


ip_token_list = [(i, j) for i in config['api_ip'] for j in config['token'] if i != j] #初始化ip和token的列表(轮询池)


actree = ahocorasick.Automaton()#初始化AC自动机
for index, word in enumerate(config['wordlist']):
    actree.add_word(word, (index, word))
actree.make_automaton() #初始化完成，一般来说重启才能重载屏蔽词



async def guolv(sent):#过滤屏蔽词
    sent_cp = sent.lower() #转为小写
    tags_guolv = ""
    for i in actree.iter(sent):
        sent_cp = sent_cp.replace(i[1][1], "")
        tags_guolv += str(i[1][1]) + " "
    return sent_cp,tags_guolv

async def process_tags(gid,uid,tags,add_db=config['add_db'],trans=config['trans'],limit_word=config['limit_word'],arrange_tags=config['arrange_tags']):
    error_msg ="" #报错信息
    tags_guolv="" #过滤词信息
    #初始化
    try:
        tags = f"tags={tags.strip().lower()}" #去除首尾空格换行#转小写#头部加上tags=
        taglist = re.split('&',tags) #分割
        id = ["tags=","ntags=","seed=","scale=","shape=","strength=","r18="]
        tag_dict = {x: "" for x in id} #初始化字典,结构为:tags+ntags+seed+scale+shape
        for i in id:
            tag_dict[i] = ("" if not [idx for idx in taglist if idx.startswith(i)] else [idx for idx in taglist if idx.startswith(i)][-1]).replace(i, '', 1) #取出tags+ntags+seed+scale+shape,每种只取列表最后一个,并删掉id
        if not tag_dict["tags="]:
            tag_dict["tags="] = config['tags_moren']
    except Exception as e:
        error_msg += f"tags初始化失败{e}"
        return tags,error_msg,tags_guolv
    #翻译tags
    if trans:
        try:
            if tag_dict["ntags="]:
                tags2trans = tag_dict["tags="]+"&"+tag_dict["ntags="] # &作为分隔符
                tags2trans = await youdao.tag_trans(tags2trans) #翻译
                taglist1 = re.split('&',tags2trans)
                tag_dict["tags="] = taglist1[0]
                tag_dict["ntags="] = taglist1[1]
            else:
                tags2trans = tag_dict["tags="]
                tags2trans = await youdao.tag_trans(tags2trans) #翻译
                tag_dict["tags="] = tags2trans
        except Exception as e:
            error_msg += "翻译失败"
            return tags,error_msg,tags_guolv
    #过滤tags
    if limit_word:
        try:
            #过滤tags,只过滤正面tags
            tags2guolv = tag_dict["tags="]
            tags2guolv,tags_guolv = await guolv(tags2guolv)#过滤
            tag_dict["tags="] = tags2guolv
        except Exception as e:
            error_msg += "过滤失败"
            return tags,error_msg,tags_guolv
    #整理tags
    if arrange_tags:
        try:
            #整理tags,只整理正面tags
            id2tidy = ["tags=","ntags="]
            for i in id2tidy:
                tidylist = re.split(',|，',tag_dict[i])
                while "" in tidylist:
                    tidylist.remove("")
                tag_dict[i] = ",".join(tidylist)
        except Exception as e:
            error_msg += f"整理失败{e}"
            return tags,error_msg,tags_guolv
    #上传XP数据库
    if add_db:
        try:
            #上传XP数据库
            tags2XP = tag_dict["tags="]
            taglist3 = re.split(',',tags2XP)
            for tag in taglist3:
                db.add_xp_num(gid,uid,tag)
        except Exception as e:
            error_msg += "上传失败"
            return tags,error_msg,tags_guolv
    #整合tags
    tags = tag_dict["tags="] if tag_dict["tags="] else config['tags_moren']
    for i in id:
        if i != "tags=" and tag_dict[i]:
            tags += "&"+i+tag_dict[i]
    tags = tags.replace("landscape", "Landscape")
    tags = tags.replace("portrait", "Portrait")
    tags = tags.replace("square", "Square")
    return tags,error_msg,tags_guolv

async def retry_get_ip_token(i):
    if i < len(ip_token_list):
        api_ip,token = ip_token_list[i]
    return api_ip,token






async def get_imgdata(tags,way=1,shape="Portrait",strength=config['strength'],b_io=None):#way=1时为get，way=0时为post
    error_msg =""  #报错信息
    result_msg = ""
    i = 0
    while i < len(ip_token_list):
        await asyncio.sleep(1) #防止过快
        i+=1
        print(f"第{i}次查询")
        api_ip,token = await retry_get_ip_token(i-1)
        try:
            if way:
                url = (f"http://{api_ip}/got_image") + (f"?tags={tags}")+ (f"&token={token}")
                response = await aiorequests.get(url, timeout=180)
            else:
                if "&strength=" in tags:
                    url = (f"http://{api_ip}/got_image2image") + (f"?tags={tags}")+(f"&shape={shape}") +(f"&token={token}")
                else:
                    url = (f"http://{api_ip}/got_image2image") + (f"?tags={tags}")+(f"&shape={shape}")+(f"&strength={strength}")+(f"&token={token}")
                response = await aiorequests.post(url,data=b64encode(b_io.getvalue()), timeout=180)
            imgdata = await response.content
            if len(imgdata) < 5000:
                error_msg = "token冷却中~"
                continue
        except Exception as e:
            error_msg = f"超时了~"
            continue
        i=999
        error_msg = ""
    try:
        msg=""
        msgdata = json.loads(re.findall('{"steps".+?}',str(imgdata))[0])
        msg = f'\nseed:{msgdata["seed"]}   scale:{msgdata["scale"]}'
    except Exception as e:
        error_msg = f"获取图片信息失败"
        return result_msg,error_msg
    try:
        img = Image.open(BytesIO(imgdata)).convert("RGB")
        buffer = BytesIO()  # 创建缓存
        img.save(buffer, format="png")
        imgmes = 'base64://' + b64encode(buffer.getvalue()).decode()
    except Exception as e:
        error_msg += "处理图像失败{e}"
        return result_msg,error_msg
    result_msg = f"[CQ:image,file={imgmes}]{msg}\ntags:{tags}"
    return result_msg,error_msg

async def get_xp_list_(msg,gid,uid):
    error_msg =""  #报错信息
    result_msg = ""
    if msg == "本群":
        xp_list = db.get_xp_list_group(gid)
    elif msg == "个人":
        xp_list = db.get_xp_list_personal(gid,uid)
    else:
        error_msg = "参数错误"
        return result_msg,error_msg
    result_msg = f'{msg}的XP排行榜为：\n'
    if len(xp_list)>0:
        for xpinfo in xp_list:
            keyword, num = xpinfo
            result_msg += f'关键词：{keyword}||次数：{num}\n'
    else:
        result_msg = f'暂无{msg}的XP信息'
    return result_msg,error_msg

async def get_xp_pic_(msg,gid,uid):
    error_msg =""  #报错信息
    result_msg = ""
    if msg == "本群":
        xp_list = db.get_xp_list_kwd_group(gid)
    elif msg == "个人":
        xp_list = db.get_xp_list_kwd_personal(gid,uid)
    else:
        error_msg = "参数错误"
        return result_msg,error_msg
    if len(xp_list)>0:
        keywordlist = []
        for (a,) in xp_list:
            keywordlist.append(a)
        tags = (',').join(keywordlist)
        result_msg = tags
    else:
        error_msg = f'暂无{msg}的XP信息'
    return result_msg,error_msg

async def get_pic_d(msg):
    error_msg = ""  # 报错信息
    b_io = ""
    shape = "Portrait"
    size = 0
    try:
        image_url = re.search(r"\[CQ:image,file=(.*)url=(.*?)[,|\]]", str(msg))
        url = image_url.group(2)
    except Exception as e:
        error_msg = "你的图片呢？"
        return b_io,shape,error_msg,size
    try:
        img_data = await aiorequests.get(url)
        image = Image.open(BytesIO(await img_data.content))
        a,b = image.size
        size = a*b
        c = a/b
        s = [0.6667,1.5,1]
        s1 =["Portrait","Landscape","Square"]
        shape=s1[s.index(nsmallest(1, s, key=lambda x: abs(x-c))[0])]#判断形状
        image = image.convert("RGB")
        b_io = BytesIO()
        image.save(b_io, format="JPEG")

    except Exception as e:
        error_msg = "图片处理失败" # 报错信息
        return b_io,shape,error_msg,size
    return b_io,shape,error_msg,size

async def img_make(msglist,page = 1):
    num = len(msglist)
    max_row = math.ceil(num/4)
    target = Image.new('RGB', (1920,512*max_row),(255,255,255))
    page = page - 1
    idlist,imglist,thumblist = [],[],[]
    for (a,b,c) in msglist:
        idlist.append(a)
        imglist.append(b)
        thumblist.append(c)
    for index in range(0+(page*config['per_page_num'])),(config['per_page_num']+(page*config['per_page_num'])):
        try:
            id = f"ID: {idlist[index]}" #图片ID
            thumb = f"点赞: {thumblist[index]}" #点赞数
            image_path= str(imglist[index]) #图片路径
        except:
            break
        region = Image.open(image_path)
        region = region.convert("RGB")
        region = region.resize((int(region.width/2),int(region.height/2)))
        font = ImageFont.truetype(font_path, 36)  # 设置字体和大小
        draw = ImageDraw.Draw(target)
        row = math.ceil((index+1)/4)
        column= (index+1)%4+1
        target.paste(region,(80*column+384*(column-1),50+100*(row-1)+384*(row-1)))
        draw.text((80*column+384*(column-1)+int(region.width/2)-90,80+100*(row-1)+384*(row-1)+region.height),id,font=font,fill = (0, 0, 0))
        draw.text((80*column+384*(column-1)+int(region.width/2)+20,80+100*(row-1)+384*(row-1)+region.height),thumb,font=font,fill = (0, 0, 0))
    result_buffer = BytesIO()
    target.save(result_buffer, format='JPEG', quality=100) #质量影响图片大小
    imgmes = 'base64://' + base64.b64encode(result_buffer.getvalue()).decode()
    result_msg = f"[CQ:image,file={imgmes}]"
    return result_msg

async def check_pic_(gid,uid,msg,page):
    error_msg = ""
    num = page*config['per_page_num']
    if msg == "本群":
        msglist = db.get_pic_list_group(gid,num)
    elif msg == "个人":
        msglist = db.get_pic_list_personal(uid,num)
    elif msg == "全部":
        msglist = db.get_pic_list_all(num)
    else:
        error_msg = "参数错误"
        return result_msg,error_msg
    if len(msglist) == 0:
        error_msg = f"无法找到{msg}图片信息"
        return result_msg,error_msg
    result_msg = await img_make(msglist,page)
    return result_msg,error_msg

async def save_pic(data):
    error_msg = ""
    pic_hash = ""
    pic_dir = ""
    try:
        pic_hash = hash(data)
        datetime = calendar.timegm(time.gmtime())
        image_path= './SaveImage/'+str(datetime)+'.jpg'
        pic_dir = join(curpath, f'{image_path}')#hash与savepath
        pic = open(pic_dir, "wb")
        pic.write(data)
        pic.close() #保存图片
    except Exception as e:
        error_msg = "图片保存失败"
        return pic_hash,pic_dir,error_msg
    return pic_hash,pic_dir,error_msg

async def get_imgdata_magic(tags):#way=1时为get，way=0时为post
    error_msg =""  #报错信息
    result_msg = ""
    i = 0
    while i < len(ip_token_list):
        await asyncio.sleep(1) #防止过快
        i += 1
        print(f"第{i}次查询")
        api_ip,token = await retry_get_ip_token(i-1)
        try:
            url = (f"http://{api_ip}/got_image") + (f"?tags={tags}")+ (f"&token={token}")
            response = await aiorequests.get(url, timeout=180)
            imgdata = await response.content
            if len(imgdata) < 5000:
                error_msg = "token冷却中~"
                continue
        except Exception as e:
            error_msg = f"超时了~"
            continue
        i=999
        error_msg = ""
    try:
        img = Image.open(BytesIO(imgdata)).convert("RGB")
        buffer = BytesIO()  # 创建缓存
        img.save(buffer, format="png")
        imgmes = 'base64://' + b64encode(buffer.getvalue()).decode()
    except Exception as e:
        error_msg += "处理图像失败{e}"
        return result_msg,error_msg
    result_msg = f"[CQ:image,file={imgmes}]"
    return result_msg,error_msg

async def img2anime_(message,msg):
    error_msg = ""
    result_msg = ""
    if not config['img2anime']:
        error_msg = "未开启动漫化功能"
        return result_msg,error_msg
    b_io,shape,error_msg,size = await get_pic_d(message)
    if error_msg != "":
        return result_msg,error_msg
    json_data = ["data:image/jpeg;base64," + base64.b64encode(b_io.getvalue()).decode()]
    result_msg,error_msg = await easygradio.quene_push_(config['img2anime_url'],json_data,max_try=config['img2anime_url_timeout'])
    if error_msg != "":
        return result_msg,error_msg
    result_img = base64.b64decode(''.join(result_msg.split(',')[1:]))
    result_img = Image.open(BytesIO(result_img)).convert("RGB")
    buffer = BytesIO()  # 创建缓存
    result_img.save(buffer, format="png")
    img_msg = 'base64://' + b64encode(buffer.getvalue()).decode()
    result_msg = f"[CQ:image,file={img_msg}]"
    return result_msg,error_msg

async def img2tags_(message,msg):
    result_msg = ""
    error_msg = "" #报错信息
    if not config['img2tag']:
        error_msg = "未开启鉴赏图片功能"
        return result_msg,error_msg
    b_io,shape,error_msg,size = await get_pic_d(message)
    if error_msg != "":
        return result_msg,error_msg
    json_data = ["data:image/jpeg;base64," + base64.b64encode(b_io.getvalue()).decode(),0.7]
    result_msg,error_msg = await easygradio.quene_push_(config['img2tags_url'],json_data,max_try=config['img2tags_url_timeout'])
    if error_msg != "":
        return result_msg,error_msg
    result_msg = result_msg['confidences']
    result_msg = ','.join([f'{i["label"]}' for i in result_msg]).replace("rating:safe,","")
    result_msg = f"\n鉴赏出的tags有:{result_msg}"
    return result_msg,error_msg

async def pic_super_(message,msg):
    error_msg = ""
    result_msg = ""
    size = 0
    if not config['picsuper']:
        error_msg = "未开启图片超分"
        return result_msg,error_msg
    b_io,shape,error_msg,size = await get_pic_d(message)
    if error_msg != "":
        return result_msg,error_msg
    if size > config['max_size']:
        error_msg = "图片这么大，进不去拉~"
        return result_msg,error_msg
    try:
        if "2倍超分" in msg:
            scale = 2
        elif "3倍超分" in msg:
            scale = 3
        elif "4倍超分" in msg:
            scale = 4
        else:
            scale = 2
        if "保守降噪" in msg:
            con = "conservative"
        elif "降噪" in msg:
            con = "denoise3x"
        else:
            con = "no-denoise"
        modelname = f"up{scale}x-latest-{con}.pth"
    except Exception as e:
        error_msg += "超分参数错误"
        return result_msg,error_msg
    json_data = ["data:image/jpeg;base64," + base64.b64encode(b_io.getvalue()).decode(),modelname,2]
    result_msg,error_msg = await easygradio.quene_push_(config['pic_super_url'],json_data,max_try=config['pic_super_timeout'])
    if error_msg != "":
        return result_msg,error_msg
    result_msg = result_msg.split("base64,")[1]
    result_msg = 'base64://' + result_msg
    result_msg = f"[CQ:image,file={result_msg}]"
    return result_msg,error_msg
