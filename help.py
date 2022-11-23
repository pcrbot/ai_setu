from PIL import Image,ImageDraw,ImageFont
import os
import math
from os.path import dirname, join, exists

curpath = dirname(__file__) #当前路径
font_path = join(curpath,"resources/font/093.ttf")  #字体文件路径
img_path = join(curpath,"resources/help/img/")  #图片文件路径

content1 = '''
绘图功能指令:

(SD)绘图 XXX
(SD)以图绘图 XXX + 图片

()内为可选 XXX为绘图参数
指令要求图片时需携带图片,也可以通过直接回复图片或CQ码

本功能是本bot的核心功能,可以绘制各种图形
默认绘图参数为miku
'''.strip()

content2 = '''
元素法典功能指令:

元素法典吟唱 XXX
元素法典咏唱 XXX
元素法典目录

XXX可以是多种魔咒,空格分离
咏唱会加入黑暗魔典内容
'''.strip()

content3 ='''
绘图参数指南:
规范：
绘图 <tags>[&shape=Portrait/Landscape/Square|&scale=11|&seed=1234]
例如：
绘图 loli,xcw,{cute}&shape=Portrait&scale=24
<tags>用,逗号分隔多个tag,加{}代表增加权重
直接输入英语,会经过自然语言处理
直接输入中文,会经过翻译和自然语言处理

[ ]为可选参数，其中：
shape 分别为竖图、横图、方图，默认竖图
scale 默认11,建议3-24
seed 默认随机种子(数字),相同的种子可能会有相同的结果
r18 默认值为0,即出安全的图片,为1时可能出现不安全图片

如果你的指令还带有前缀SD
那么可选参数有:
["tags=","ntags=","seed=","scale=","shape=",
"strength=","r18=","steps=","sampler=",
"restore_faces=","tiling=","bigger="]

以上参数自行探索
'''.strip()

content4 ='''
杂项功能指令:
超分pic 2/3/4倍超分 (专业) 保守/3倍/无降噪 + 图片
动漫化 + 图片
鉴赏图片 + 图片

()内为可选 XXX为绘图参数 /为可替换参数
指令要求图片时需携带图片,也可以通过直接回复图片或CQ码
'''.strip()

content5 ='''
'水魔法', '空间法', '冰魔法', '核爆法', '风魔法', 
'流沙法', '白骨法', '星空法', '机凯种', '森林冰', 
'幻之时', '雷男法', '圣光法', '苇名法', '自然法', 
'冰系改', '融合法', '虹彩法', '暗锁法', '星冰乐', 
'火烧云', '城堡法', '雪月法', '结晶法', '黄昏法', 
'森林法', '泡泡法', '蔷薇法', '月亮法', '森火法', 
'废土法', '机娘水', '黄金法', '死灵法', '水晶法', 
'水森法', '冰火法', '龙骑士', '坠落法', '水下法', 
'秘境法', '摄影法', '望穿水', '天选术', '摩登法', 
'血魔法', '绚丽术', '唤龙术', '龙机法', '战姬法', 
'炼银术', '星源法', '学院法', '浮世绘', '星霞海', 
'冬雪法', '刻刻帝', '万物熔炉', '暗鸦法', '花火法基础', 
'星之彩', '沉入星海', '百溺法', '百溺法plus', '辉煌阳光法', 
'星鬓法', '森罗法', '星天使', '黄金律', '机凯姬 改', 
'人鱼法', '末日', '碎梦', '幻碎梦', '血法改', 
'留影术', '西幻术', '星语术', '金石法', '飘花法', 
'冰霜龙息plus', '冰霜龙息', '白虎志', '狡兽录', '穷奇录', 
'故障艺术', '立体主义', '嘻哈风', '默剧法', '漫画风格', 
'彩色漫画风格', '彩墨法', '繁浮法', '琉璃法', '半厚涂', 
'古典肖像法', '古典肖像法plus', '跑团法', '太空兔', '人像水墨法', 
'断墨残楮', '断墨残楮-花青水', '断墨残楮-胭脂红', '断墨残楮-彩', '像素法', 
'工程设计', '世界文化-中式壁画', '世界文化-埃及壁画', '世界文化-教堂壁画', '世界文化-街头涂鸦', 
'世界文化-剪纸窗花', '世界文化-彩绘玻璃', '世界文化-铸币', '机魂法', '失落之海', 
'深海巨物恐惧症', '萝卜法', '灵铠法', '星战法 2.0', '巨星法', 
'黑洞法', '开席术', '徽章法', '积木法', '美术场景法', 
'水镜法', '天堂台阶-人物', '天堂台阶-景物', '中国龙', '蒸汽朋克', 
'恶魔·深渊', '彩漆法', '今宵绝唱', '军姬法', '小小弥赛亚', 
'黄金叶', '林奈法-植物', '林奈法-人物', '桃法', '春之貓', 
'夏夜之狐', '描背法', '塔罗牌术', '群像法', '瑞雪兆丰年', 
'古典系', '圣宫法', '向日葵法', '人偶法', '圣经', 
'怨念芷', '蜂女术', '触手法', '大威天龙', '寂雨', 
'彷徨', '星际穿越', '龙女幻想', '国风少女', '樱乐会', 
'瓶中法', '未名花', '未名雨', '云海白鹤', '下午茶', 
'孔雀仙', '彻夜之歌', '潘多拉猫法2.0', '冰与火之歌', '铁驭术', 
'冰箱贴', '靛金术', '发光二极管', '古卷魔女', '鬼火骷髅法', 
'黑洞构成法', '灭世魔神', '伏魔经', '立绘法', '蘑菇森林法', 
'暗海术', '秋水之淚', '冬雪之兔', '赛博chibi', '沙画法', 
'AI鬼画符在线掐诀', '山水小注', '深秋枫庭', '时代之风', '兽灵术', 
'水龙吟', '水裙法', '黑蛊', '佛 法', '卧狐', 
'闲潭梦花', '星际公民法', '虚无之境', '游戏人间', '银河潜航', 
'手绘法', '元素幻兽-地', '元素幻兽-水', '元素幻兽-火', '元素幻兽-风', 
'阈限空间-怪核', '阈限空间-梦核', '阈限空间-伤核', '阈限空间-池核', '阈限空间-网核', 
'源宝病毒', '月下湖中仙女', '云作壁上观-木刻', '云作壁上观-石刻', '云作壁上观-木壁', 
'中国道家古风', '真空管', '自走棋', '世界终焉', '天国'
'''.strip()



def get_png(i):
    if i==7:
      i=1
    img = f"{img_path}/help{i}.png"
    i+=1
    return img,i

def get_wide(str_str) :
    count = 0
    if str == type(str_str) :
        for str_tmp in str_str :
            if ord(str_tmp) - ord('0') >= 128 :
                count += 1
    wide = math.ceil((len(str_str) - count)*25.75 + count*50) + 50 #60px的画笔 + 50px的边距(中文42.25px,英文25.75px)
    return wide

def draw_it(contentlist:list,name:str):
    contentlist = contentlist
    maxheight = 0
    maxwidth = 0
    for i in contentlist:
        maxheight += (i.count('\n')+1)*60 + 300  #计算文本最大高度
        nowwideth = max([get_wide(i) for i in i.split('\n')])
        if maxwidth < nowwideth:
            maxwidth = nowwideth
    #im = Image.new("RGBA",[30+maxwidth+30,maxheight+100],"white")
    im = Image.open(f"{img_path}/background.png").convert('RGBA')
    im = im.resize((30+maxwidth+30, maxheight+100),Image.Resampling.LANCZOS)
    drawObj = ImageDraw.Draw(im)
    height = 0
    j=1
    for i in contentlist:
        img,j = get_png(j)
        im2 = Image.open(img).convert('RGBA')
        x,y = im2.size
        im2 = im2.resize((maxwidth+20, y),Image.Resampling.LANCZOS)
        r, g, b, a = im2.split() #去除黑边
        im.paste(im2,(30,height),mask=a)
        w_height = (i.count('\n')+1)*60+170 # 计算文本行数
        img,j = get_png(j)
        im3 = Image.open(img).convert('RGBA')
        im3 =  im3.resize((maxwidth+20, w_height),Image.Resampling.LANCZOS)
        r, g, b, a = im3.split()
        im.paste(im3,(30,height+y),mask=a)
        font = ImageFont.truetype(font_path, 60, encoding="utf-8")#每字约为21px宽,创建画笔
        drawObj.text((30+55,height+y+15), i, 'black', font)#写入文本
        height += w_height+150 #+150
    im.convert('RGB').save(f'{name}.jpg', quality=75)

def 救命啊():
    contentlist = [content1,content2,content3,content4]
    draw_it(contentlist,f"{curpath}/help_main")
    contentlist = [content5]
    draw_it(contentlist,f"{curpath}/magic")