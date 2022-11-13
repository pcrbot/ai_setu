# 2022.10.14 18:07
import re
from hoshino import Service, priv
from . import db,until,help


sv_help = '''
[帮助 绘图]查看帮助
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
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=help.help_msg_all)


@sv.on_prefix('绘图')
async def text2img(bot, ev):
    #await bot.send(ev, f"收到指令,处理中~", at_sender=True) #触发回馈示例,喜欢就取消注释
    gid = ev.group_id
    uid = ev.user_id
    tags = ev.message.extract_plain_text().strip()
    tag_dict,error_msg,tags_guolv=await until.process_tags(gid,uid,tags) #tags处理过程
    if len(error_msg):
        await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolv):
        await bot.send(ev, f"已过滤：{tags_guolv}", at_sender=True)
    result_msg,error_msg = await until.get_imgdata(tag_dict,way=0)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    #result_msg = f"[CQ:reply,id={ev.message_id}]{result_msg}"     #回复形式发送,喜欢就取消注释,并注释下一行
    await bot.send(ev, result_msg, at_sender=True)


@sv.on_prefix('SD绘图')
async def text2img_sd(bot, ev):
    #await bot.send(ev, f"收到指令,处理中~", at_sender=True) #触发回馈示例,喜欢就取消注释
    gid = ev.group_id
    uid = ev.user_id
    tags = ev.message.extract_plain_text().strip()
    tag_dict,error_msg,tags_guolv=await until.process_tags(gid,uid,tags) #tags处理过程
    if len(error_msg):
        await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolv):
        await bot.send(ev, f"已过滤：{tags_guolv}", at_sender=True)
    result_msg,error_msg = await until.get_imgdata_sd(tag_dict,way=0)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    #result_msg = f"[CQ:reply,id={ev.message_id}]{result_msg}"     #回复形式发送,喜欢就取消注释,并注释下一行
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
    tag_dict,error_msg,tags_guolv=await until.process_tags(gid,uid,tags) #tags处理过程
    if len(error_msg):
        await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolv):
        await bot.send(ev, f"已过滤：{tags_guolv}", at_sender=True)
    result_msg,error_msg = await until.get_imgdata_sd(tag_dict,way=1,shape=shape,b_io=b_io,size=size) #绘图过程
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    await bot.send(ev, result_msg, at_sender=True)


@sv.on_keyword("解析pic")
async def get_pic_msg(bot, ev):
    if ev.message[0].type == "reply":
        tmsg = await bot.get_msg(message_id=int(ev.message[0].data['id']))
        ev.message = tmsg["message"]
    msg = await until.get_pic_msg_temp(ev.message)
    await bot.send(ev, msg, at_sender=True)






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
    tag_dict,error_msg,tags_guolv=await until.process_tags(gid,uid,tags,add_db=0,arrange_tags=0) #tags处理过程
    if len(error_msg):
        await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolv):
        await bot.send(ev, f"已过滤：{tags_guolv}", at_sender=True)
    result_msg,error_msg = await until.get_imgdata(tag_dict)
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


@sv.on_prefix(('查看pic'))
async def check_pic(bot, ev):
    gid = ev.group_id
    uid = ev.user_id
    msg = ev.message.extract_plain_text()
    result_msg,error_msg = await until.check_pic_(gid,uid,msg)
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
    tag_dict,error_msg,tags_guolv=await until.process_tags(gid,uid,tags) #tags处理过程
    if len(error_msg):
        await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolv):
        await bot.send(ev, f"已过滤：{tags_guolv}", at_sender=True)
    result_msg,error_msg = await until.get_imgdata(tag_dict)
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




















@sv.on_prefix("元素法典")
async def magic_book(bot, ev):
    msg = ev.message.extract_plain_text().strip()
    if msg == "目录":
        msg =f"元素法典目录:\n{str(until.magic_data_title)}"
        await bot.finish(ev, msg, at_sender=True)
    tag_dict,error_msg = await until.get_magic_book_(msg)
    if len(error_msg):
        await bot.finish(ev, f"{error_msg}", at_sender=True)
    result_msg,error_msg = await until.get_imgdata(tag_dict)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    await bot.send(ev, result_msg, at_sender=True)


@sv.on_prefix("SD元素法典")
async def magic_book_sd(bot, ev):
    msg = ev.message.extract_plain_text().strip()
    if msg == "目录":
        msg =f"元素法典目录:\n{str(until.magic_data_title)}"
        await bot.finish(ev, msg, at_sender=True)
    tag_dict,error_msg = await until.get_magic_book_(msg)
    if len(error_msg):
        await bot.finish(ev, f"{error_msg}", at_sender=True)
    result_msg,error_msg = await until.get_imgdata_sd(tag_dict,way=0)
    if len(error_msg):
        await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
    await bot.send(ev, result_msg, at_sender=True)


















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