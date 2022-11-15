from hoshino import aiorequests
import uuid
import asyncio

'''
gradio 调用api的方法,大概通用
'''

'''async def quene_fetch_(url,_hash,max_try):
    #报错信息
    result_msg = ""
    error_msg = ""
    i = 0
    url_status = f'{url}/api/queue/status/'
    while i< max_try :
        i+=1
        resj =  await (await aiorequests.post(url_status, json={'hash': _hash})).json()
        await asyncio.sleep(1)#等待1秒
        if resj['status'] == 'PENDING' or resj['status'] == 'QUEUED':
            error_msg = f"状态码:{resj['status']} 原因:超时了捏~"
            continue
        elif resj['status'] == 'COMPLETE':
            error_msg = ""
            #print(resj['data']['data'])
            result_msg = resj['data']['data'] #获取结果 resj['data']['data']
            return result_msg,error_msg
        else:
            error_msg = f"状态码:{resj['status']} 失败原因:{resj['data']}"
            return result_msg,error_msg

async def quene_push_(url,json_data,max_try=60):
    result_msg = ""
    error_msg = ""
    url_push = f'{url}/api/queue/push/'
    json = {
        "fn_index": 0,
        "data": json_data,
        "session_hash": str(uuid.uuid1()),
        "action": "predict"
    }
    try:
        _hash = (await(await aiorequests.post(url_push, json=json)).json())['hash'] #获取当前任务的hash
    except Exception as e:
        error_msg = f"尝试排队 失败原因:{e}"
        return result_msg,error_msg
    max_try= max_try
    result_msg,error_msg = await quene_fetch_(url,_hash,max_try) #获取结果 resj['data']['data'][0]
    return result_msg,error_msg'''


async def predict_push_(url,json_data,max_try=60):
    result_msg = ""
    error_msg = ""
    url_predict = url
    json = {
        "session_hash": str(uuid.uuid1()),
        "data": json_data,
        "fn_index": 0
    }
    await asyncio.sleep(1)#等待1秒
    try:
        resj = await (await aiorequests.post(url_predict, json=json,timeout = max_try)).json()
    except Exception as e:
        error_msg = f"请求失败 失败原因:{e}"
    try:
        result_msg = resj['data']
    except Exception as e:
        error_msg = f"请求失败 失败原因:{e},获取内容{resj}"
    return result_msg,error_msg
