# 2022.10.14 18:07
import re
from hoshino import Service, priv
from . import db,until


sv_help = '''
主要功能：
【绘图 XXX】
【以图绘图 XXX 图片】
【本群/个人XP排行】
【本群/个人XP缝合】
【绘图参数指南】
【元素法典指南】
【上传pic】务必携带seed/scale/tags等参数
【查看本群pic】
【点赞pic xxx】
'''.strip()

sv_help1 = '''
规范：绘图 <tags>[&shape=Portrait/Landscape/Square|&scale=11|&seed=1234]
例如：绘图 loli,xcw&shape=Portrait&scale=24
<tags>为必选参,逗号分隔tag,%20为空格转义,加0代表增加权重,可以加很多个,可直接英语句子
[ ]为可选参数，其中：
tags 图片含有的要素，使用大括号{}括住某些tag来增加此tag的权重，括号越多权重越高如{{{loli}}}
shape 分别为竖图、横图、方图，默认竖图
scale 默认11,只建议11-24,细节会提高,太高了会过曝
seed 随机种子，任意数字。相同的种子可能会有相同的结果
'''.strip()

sv_help2 ='''
【元素法典目录】
【元素法典吟唱 XXX】
【元素法典吟唱 融合魔法 XXX XXX】
'''.strip()

sv_help3 ='''元素法典目录:
['水魔法', '空间法', '冰魔法', '核爆法', '风魔法', '流沙法', '白骨法', '星空法', '机凯种', '森林冰', '幻之时', '雷男法', '圣光法', '苇名法', '自然法', '冰系改', '融合法', '虹彩法', '暗锁法', '星冰乐', '火烧云', '城堡法', '雪月法', '结晶法', '黄昏法', '森林法', '泡泡法', '蔷薇法', '月亮法', '森火法', '废土法', '机娘水', '黄金法', '死灵法', '水晶法', '水森法', '冰火法', '龙骑士', '坠落法', '水下法', '秘境法', '摄影法', '望穿水', '天选术', '摩登法', '血魔法', '绚丽术', '唤龙术', '龙机法', '战姬法', '炼银术', '星源法', '学院法', '浮世绘', '星霞海', '冬雪法', '刻刻帝', '万物熔炉', '暗鸦法', '花 火法基础', '星之彩', '沉入星海', '百溺法', '百溺法plus', '辉煌阳光法', '星鬓法', '森罗法', '星天使', '黄金律', '机凯姬 改', '人鱼法', '末日', '碎梦', '幻碎梦', '血法改', '留影术', '西幻术', '星语术', '金石法', '飘花法', '冰霜龙息plus', '冰霜龙息']
'''.strip()


sv = Service(
    name = '绘图',  #功能名
    use_priv = priv.NORMAL, #使用权限
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = True, #是否默认启用
    bundle = '娱乐', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助 绘图"])
async def cwbangzhu(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)

@sv.on_fullmatch(["绘图参数指南"])
async def cwbangzhu12(bot, ev):
    await bot.send(ev, sv_help1, at_sender=True)

@sv.on_fullmatch(["元素法典指南"])
async def cwbangzhu13(bot, ev):
    await bot.send(ev, sv_help2, at_sender=True)

@sv.on_fullmatch(["元素法典目录"])
async def cwbangzhu14(bot, ev):
    await bot.send(ev, sv_help3, at_sender=True)


@sv.on_prefix('绘图')
async def text2img(bot, ev):
    #await bot.send(ev, f"收到指令,处理中~", at_sender=True) #触发回馈示例,喜欢就取消注释
    gid = ev.group_id
    uid = ev.user_id
    tags = ev.message.extract_plain_text().strip()
    tags,error_msg,tags_guolv=await until.process_tags(gid,uid,tags) #tags处理过程
    if len(error_msg):
        await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolv):
        await bot.send(ev, f"已过滤：{tags_guolv}", at_sender=True)
    result_msg,error_msg = await until.get_imgdata(tags)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    #result_msg = f"[CQ:reply,id={ev.message_id}]{result_msg}"     #回复形式发送
    await bot.send(ev, result_msg, at_sender=True)

@sv.on_keyword("以图绘图")
async def img2img(bot, ev):
    gid = ev.group_id
    uid = ev.user_id
    tags = ev.message.extract_plain_text().replace("以图绘图","").strip()
    if ev.message[0].type == "reply":
        tmsg = await bot.get_msg(message_id=int(ev.message[0].data['id']))
        ev.message = tmsg["message"]
    b_io,shape,error_msg,size = await until.get_pic_d(ev.message)  #图片获取过程
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    tags,error_msg,tags_guolv=await until.process_tags(gid,uid,tags) #tags处理过程
    if len(error_msg):
        await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolv):
        await bot.send(ev, f"已过滤：{tags_guolv}", at_sender=True)
    result_msg,error_msg = await until.get_imgdata(tags,way=0,shape=shape,b_io=b_io) #绘图过程
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    await bot.send(ev, result_msg, at_sender=True)

@sv.on_suffix('XP排行')
async def get_xp_list(bot, ev):
    msg = ev.message.extract_plain_text()
    gid = ev.group_id
    uid = ev.user_id
    result_msg,error_msg = await until.get_xp_list_(msg,gid,uid)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    await bot.send(ev, result_msg, at_sender=True)

@sv.on_suffix('XP缝合')
async def get_xp_pic(bot, ev):
    gid = ev.group_id
    uid = ev.user_id
    msg = ev.message.extract_plain_text()
    tags,error_msg = await until.get_xp_pic_(msg,gid,uid)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    tags,error_msg,tags_guolv=await until.process_tags(gid,uid,tags,add_db=0,arrange_tags=0) #tags处理过程
    if len(error_msg):
        await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolv):
        await bot.send(ev, f"已过滤：{tags_guolv}", at_sender=True)
    result_msg,error_msg = await until.get_imgdata(tags)
    await bot.send(ev, result_msg, at_sender=True)



@sv.on_keyword('上传pic')
async def upload_header(bot, ev):
    if ev.message[0].type == "reply":
        tmsg = await bot.get_msg(message_id=int(ev.message[0].data['id']))
        ev.message = tmsg["message"]
    b_io,shape,error_msg,size = await until.get_pic_d(ev.message)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    data = b_io.getvalue()
    pic_hash,pic_dir,error_msg = await until.save_pic(data)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    try:
        seed=(str(ev.message).split(f"scale:")[0]).split('seed:')[1].strip()
        scale=(str(ev.message).split(f"tags:")[0]).split('scale:')[1].strip()
        tags=(str(ev.message).split(f"tags:")[1])
        pic_msg = tags + f"&seed={seed}" + f"&scale={scale}"
    except:
        await bot.finish(ev, '格式出错', at_sender=True)
    try:
        db.add_pic(ev.group_id, ev.user_id, pic_hash, pic_dir, pic_msg)
        await bot.send(ev, f'上传成功！', at_sender=True)
    except Exception as e:
        await bot.send(ev, f"报错:{e}",at_sender=True)


@sv.on_rex((r'^查看(.*)pic+( ([0-9]\d*))?'))
async def check_pic(bot, ev):
    gid = ev.group_id
    uid = ev.user_id
    match = ev['match']
    msg = match.group(1)
    try:
        page = int(match.group(2).lstrip())
    except:
        page = 1
    result_msg,error_msg = await until.check_pic_(gid,uid,msg,page)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    await bot.send(ev, result_msg, at_sender=True)

@sv.on_rex((r'^快捷绘图 ([0-9]\d*)(.*)'))
async def quick_img(bot, ev):
    gid = ev.group_id
    uid = ev.user_id
    match = ev['match']
    id = match.group(1)
    tags = match.group(2)
    msg = db.get_pic_data_id(id)
    (a,b) = msg
    msg = re.sub("&seed=[0-9]\d*", "", b, count=0, flags=0)
    tags +=f",{msg}"
    tags,error_msg,tags_guolv=await until.process_tags(gid,uid,tags) #tags处理过程
    if len(error_msg):
        await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolv):
        await bot.send(ev, f"已过滤：{tags_guolv}", at_sender=True)
    result_msg,error_msg = await until.get_imgdata(tags)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    await bot.send(ev, result_msg, at_sender=True)


@sv.on_prefix("点赞pic")
async def img_thumb(bot, ev):
    id = ev.message.extract_plain_text().strip()
    if not id.isdigit() and '*' not in id:
        await bot.finish(ev, '图片ID???')
    msg = db.add_pic_thumb(id)
    await bot.send(ev, msg, at_sender=True)

@sv.on_prefix("删除pic")
async def del_img(bot, ev):
    if not priv.check_priv(ev,priv.SUPERUSER):
        msg = "只有超管才能删除"
        await bot.finish(ev, msg, at_sender=True)
    id = ev.message.extract_plain_text().strip()
    if not id.isdigit() and '*' not in id:
        await bot.finish(ev, '图片ID???')
    msg = db.del_pic(id)
    await bot.send(ev, msg, at_sender=True)

@sv.on_prefix("元素法典吟唱")
async def magic_book(bot, ev):
    msg = ev.message.extract_plain_text().strip()
    tags,error_msg,node_data = await until.get_magic_book_(msg)
    if len(error_msg):
        await bot.finish(ev, f"{error_msg}", at_sender=True)
    result_msg,error_msg = await until.get_imgdata_magic(tags)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    await bot.send(ev, result_msg, at_sender=True)
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=node_data)#发送tags,用转发消息



@sv.on_keyword("鉴赏图片")
async def img2tags(bot, ev):
    msg = ev.message.extract_plain_text()
    if ev.message[0].type == "reply":
        tmsg = await bot.get_msg(message_id=int(ev.message[0].data['id']))
        ev.message = tmsg["message"]
    result_msg,error_msg = await until.img2tags_(ev.message,msg)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    await bot.send(ev, result_msg, at_sender=True)

@sv.on_keyword('超分pic')
async def get_pic_super(bot, ev):
    msg = ev.message.extract_plain_text()
    if ev.message[0].type == "reply":
        tmsg = await bot.get_msg(message_id=int(ev.message[0].data['id']))
        ev.message = tmsg["message"]
    result_msg,error_msg = await until.pic_super_(ev.message,msg)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    await bot.send(ev, result_msg, at_sender=True)

@sv.on_keyword("动漫化")
async def img2anime(bot, ev):
    msg = ev.message.extract_plain_text()
    if ev.message[0].type == "reply":
        tmsg = await bot.get_msg(message_id=int(ev.message[0].data['id']))
        ev.message = tmsg["message"]
    result_msg,error_msg = await until.img2anime_(ev.message,msg)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    await bot.send(ev, result_msg, at_sender=True)