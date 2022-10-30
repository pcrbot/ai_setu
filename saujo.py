import random
from hoshino import Service, priv
from . import until
import time
import json
from os.path import dirname, join, exists

date = True

sv_help = '''
今天我要变成少女!
今天我是什么少女
'''.strip()

sv = Service(
    name = '今天也是少女',  #功能名
    use_priv = priv.NORMAL, #使用权限
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )

curpath = dirname(__file__) #当前路径
tag_path = join(curpath,"tag_data.json")
with open((tag_path),encoding="utf-8") as f: #初始化tags
    tag_data = json.load(f)
tags_id = ["优秀实践","风格","头发","发色","衣服","鞋子","装饰","胸","类型","身份","表情","二次元","基础动作","手动作","腿动作","复合动作","露出","场景","物品","天气","环境"]
tags = "{{highly detailed}},{{masterpiece}},{ultra-detailed},{illustration},{{1girl}},{{best quality}}" #正面默认tags
ntags = "lowres,bad anatomy,bad hands,text,error,missing fingers,extra digit,fewer digits,cropped,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,username,blurry,missing arms,long neck,Humpbacked" #负面默认tags

'''@sv.on_prefix(('今天你是什么少女'))
async def say_sorry(bot, ev):
    uid = ev.user_id
    sid = None
    gid = ev.group_id
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            sid = int(m.data['qq'])
        elif m.type == 'at' and m.data['qq'] == 'all':
            await bot.send(ev, '大家都变少女了~', at_sender=True)
            return
    if sid is None:
        await bot.finish(ev, '后面跟要@的人', at_sender=True)
    data1 = await bot.get_group_member_info(group_id = gid, user_id = sid)
    name = data1['card'] if len(data1['card']) != 0 else data1['nickname']
    msg = format_msg(sid, name)
    await bot.send(ev, msg)'''
async def be_girl(uid):
    tags = ""
    goal_tag = {}
    uid = int(uid)
    random.seed(uid * (int(time.time()/3600/24)))
    for i in tags_id:
        tag_list = []
        for j in tag_data[i]:
            tag_list.append(j)
        goal_tag[i] = random.choice(tag_list)
    for i in goal_tag:
        tags += "," + tag_data[i][goal_tag[i]]
    msg = f'头发是{goal_tag["发色"]}{goal_tag["头发"]},胸部{goal_tag["胸"]},穿着{goal_tag["衣服"]},{goal_tag["鞋子"]},{goal_tag["装饰"]},萌点是{goal_tag["二次元"]},身份是{goal_tag["身份"]}{goal_tag["类型"]}'
    return msg,tags

@sv.on_fullmatch(('今天我要变成少女!','今天我是什么少女'))
async def say_sorry_me(bot, ev):
    uid = ev.user_id
    gid = ev.group_id
    name = ev.sender['nickname']
    msg,tags = await be_girl(uid)
    tags,error_msg,tags_guolv=await until.process_tags(gid,uid,msg) #tags处理过程
    if error_msg:
        await bot.finish(ev, error_msg)
    result_msg,error_msg = await until.get_imgdata_magic(tags) #图片处理过程
    if error_msg:
        await bot.finish(ev, error_msg)
    msg = f"二次元少女{name},{msg}"
    msg = msg+ result_msg
    await bot.send(ev, msg)