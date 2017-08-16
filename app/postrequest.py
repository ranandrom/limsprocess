#coding:utf-8
import requests
import datetime


headers = {"Accept": "text/plain, */*",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "zh-CN,zh;q=0.8",
           "Referer": "http://120.25.193.203:8080/anchordx-lims/",
           "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
           "Content-Type": "application/x-www-form-urlencoded",
           "X-Requested-With": "XMLHttpRequest",
           "Content-Length": "34",
           "Connection": "keep-alive",
           }

def lims_login(un, pwd):
    url_login = "http://120.25.193.203:8080/anchordx-lims/action.sys?cmd=loginManager&docmd=checkLogin&flag=1"


    limssession = requests.Session()


    postData = {
        'accountName': un,
        'password': pwd,

    }

    loginPost = limssession.post(url_login, postData, headers=headers)

    return limssession

def post_project(session):
    url = "http://120.25.193.203:8080/anchordx-lims/workflow/subs/klims/project/form/sqlservlet.W?cmd=project_object&docmd=flw_save_go"
    postData = {
        'FLWUUID':'',
        'FLWUUIDS':'',
        'OBJ_YW_ID':'',
        'OBJ_YW_BFID':'',
        'OBJ_ID':'',
        'OBJ_BFID':'',
        'PPOINT_ID':'05da9757-46c2-44e1-91e0-31d07e0595ce',
        'ITEM_ID':'44878766-8f9b-46c8-96da-0b524edea2c5',
        'WMAIN_ID':'ad016088-95f1-4f41-8786-9b0c55e31fa8',
        'isFirstPoint':0,
        'OBJ_TXT1':'',
        'OBJ_TXT2':'',
        'OBJ_TXT3':'',
        'buttonFlag':0,
        'isStart':0,
        'ID':'',
        'PJ_CODE':get_project_code(session),
        'PJ_NAME':'test2',
        'PJ_HT_ID':'',
        'PJ_TYPE':'小RNA',
        'PJ_CONTRACT_NAME':'无',
        'PJ_CUSTOMER_UNIT':'',
        'PJ_CUSTOMER_ID':'',
        'PJ_SPECIES':'',
        'PJ_BEGIN_DATE':'',
        'PJ_END_DATE':'',
        'PJ_ACTION_EXPT':'无',
        'G_STID':'',
        'PJ_PROJECT_TRACKER_NAME':'无',
        'PJ_SK':1000,
        'PJ_SKDATE': datetime.datetime.now().strftime('%Y-%m-%d'),
        'PJ_WK':'',
        'PJ_WKDATE':'',
        'PJ_ACTION_AGORA':'',
        'SAMPLE_DEAL':'保存',
        'PJ_CONTRACT_MONEY':'',
        'PJ_BEWRITE':'',
        'PJ_EXPLAIN':'',
        'PJ_REAMRK':'',
        'isSelft':'Y',
        'OTHERFLAG':'undefined',
    }

    loginPost = session.post(url, postData, headers=headers)

    return loginPost.status_code

def get_project_code(session):
    url = "http://120.25.193.203:8080/anchordx-lims/workflow/subs/klims/project/form/sqlservlet.do?cmd=getOrderCode&docmd=universalProduceCode&codeType=%25E9%25A1%25B9%25E7%259B%25AE%25E7%25BC%2596%25E5%258F%25B7"
    ordercode = session.post(url)
    return ordercode.content
