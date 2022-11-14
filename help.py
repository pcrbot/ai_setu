content1 = '''
主要功能：
【绘图 XXX】
【以图绘图 XXX 图片】
【本群/个人XP排行】
【本群/个人XP缝合】
【上传pic】务必携带seed/scale/tags等参数
【查看pic 本群/个人/全部 页码】
【点赞pic xxx】
'''.strip()

content2 = '''
绘图参数指南:
规范：绘图 <tags>[&shape=Portrait/Landscape/Square|&scale=11|&seed=1234]
例如：绘图 loli,xcw&shape=Portrait&scale=24
<tags>为必选参,逗号分隔tag,%20为空格转义,加0代表增加权重,可以加很多个,可直接英语句子
[ ]为可选参数，其中：
tags 图片含有的要素，使用大括号{}括住某些tag来增加此tag的权重，括号越多权重越高如{{{loli}}}
shape 分别为竖图、横图、方图，默认竖图
scale 默认11,只建议11-24,细节会提高,太高了会过曝
seed 随机种子，任意数字。相同的种子可能会有相同的结果
'''.strip()

content3 ='''
元素法典指南
【元素法典吟唱 XXX】XXX可以是多种魔咒,空格分离
'''.strip()

content4 ='''
元素法典目录
['水魔法', '空间法', '冰魔法', '核爆法', '风魔法', '流沙法', '白骨法', '星空法', '机凯种', '森林冰', '幻之时', '雷男法', '圣光法', '苇名法', '自然法', '冰系改', '融合法', '虹彩法', '暗锁法', '星冰乐', '火烧云', '城堡法', '雪月法', '结晶法', '黄昏法', '森林法', '泡泡法', '蔷薇法', '月亮法', '森火法', '废土法', '机娘水', '黄金法', '死灵法', '水晶法', '水森法', '冰火法', '龙骑士', '坠落法', '水下法', '秘境法', '摄影法', '望穿水', '天选术', '摩登法', '血魔法', '绚丽术', '唤龙术', '龙机法', '战姬法', '炼银术', '星源法', '学院法', '浮世绘', '星霞海', '冬雪法', '刻刻帝', '万物熔炉', '暗鸦法', '花火法基础', '星之彩', '沉入星海', '百溺法', '百溺法plus', '辉煌阳光法', '星鬓法', '森罗法', '星天使', '黄金律', '机凯姬 改', '人鱼法', '末日', '碎梦', '幻碎梦', '血法改', '留影术', '西幻术', '星语术', '金石法', '飘花法', '冰霜龙息plus', '冰霜龙息', '白虎志', '狡兽录', '穷奇录', '故障艺术', '立体主义', '嘻哈风', '默剧法', '漫画风格', '彩色漫画风格', '彩墨法', '繁浮法', '琉璃法', '半厚涂', '古典肖 像法', '古典肖像法plus', '跑团法', '太空兔', '人像水墨法', '断墨残楮', '断墨残楮-花青水', '断墨残楮-胭脂红', '断墨残楮-彩', '像素法', '工程设计', '世界文化-中式壁画', '世界文化-埃及壁画', '世界文化- 教堂壁画', '世界文化-街头涂鸦', '世界文化-剪纸窗花', '世界文化-彩绘玻璃', '世界文化-铸币', '机魂法', '失落之海', '深海巨物恐惧症', '萝卜法', '灵铠法', '星战法 2.0', '巨星法', '黑洞法', '开席术', '徽 章法', '积木法', '美术场景法', '水镜法', '天堂台阶-人物', '天堂台阶-景物', '中国龙', '蒸汽朋克', '恶魔·深渊', '彩漆法', '今宵绝唱', '军姬法', '小小弥赛亚', '黄金叶', '林奈法-植物', '林奈法-人物', '桃法', '春之貓', '夏夜之狐', '描背法', '塔罗牌术', '群像法', '瑞雪兆丰年', '古典系', '圣宫法', '向日葵法', '人偶法', '圣经', '怨念芷', '蜂女术', '触手法', '大威天龙', '寂雨', '彷徨', '星际穿越', '龙女 幻想', '国风少女', '樱乐会', '瓶中法', '未名花', '未名雨']
'''.strip()

content5 ='''
额外功能:
【超分pic xxx】
【鉴赏图片 xxx】
【动漫化 xxx】
自行探索哦~
'''.strip()

help_msg1={
        "type": "node",
        "data": {
            "name": '绘图导师小冰',
            "uin": '2854196306',
            "content": content1
        }
  }
help_msg2={
        "type": "node",
        "data": {
            "name": '绘图导师小冰',
            "uin": '2854196306',
            "content": content2
        }
  }
help_msg3={
        "type": "node",
        "data": {
            "name": '绘图导师小冰',
            "uin": '2854196306',
            "content": content3
        }
  }
help_msg4={
        "type": "node",
        "data": {
            "name": '绘图导师小冰',
            "uin": '2854196306',
            "content": content4
        }
  }
help_msg5={
        "type": "node",
        "data": {
            "name": '暴躁的镜华',
            "uin": '1764461263',
            "content": content5
        }
  }
help_msg_all = [help_msg1,help_msg2,help_msg3,help_msg4,help_msg5]
