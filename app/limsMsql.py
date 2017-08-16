#coding:utf8
'''
具体操作函数
'''

from lightMysql import LightMysql
# from flask_mysqldb import MySQL
import json
from datetime import datetime

# 配置信息，其中host, port, user, passwd, db为必需
dbconfig = {'host': '120.25.193.203',
            'port': 3306,
            'user': 'anchordx',
            'passwd': 'anchordx',
            'db': 'kmedic_tab',
            'charset': 'utf8'}


#本地开发配置
# dbconfig = {'host': '127.0.0.1',
#             'port': 3306,
#             'user': 'root',
#             'passwd': '123456',
#             'db': 'kmedic_tab',
#             'charset': 'utf8'}



db = LightMysql(dbconfig)  # 创建LightMysql对象，若连接超时，会自动重连


#样本状态
state_list = {
    0:u'收样登记', #0
    1:u'收样审核',#1
    2:u'信息录入',#2
    2.1:u'血浆分离',
    2.2:u'DNA提取',
    2.3:u'文库构建',
    2.4:u'上机测序',
    2.5:u'生信分析',
    2.6:u'暂停检测',
    3:u'检测结果',#3
    4:u'生成报告',#4
    5:u'报告发送',#5
    6:u'结束',#6
    -1:u'批量收样登记',#1
    -2:u'批量收样审核',#2
}


#项目状态
project_state_list = {
    -1: u'登记审核中',  # 0
    -2: u'登记审核中',  # 1
    0: u'登记审核中',  # 1
    1: u'登记审核中',  # 2
    2: u'实验中',  # 2
    3: u'检测分析中',  # 3
    4: u'报告中',  # 4
    5: u'报告中',  # 4
    6: u'结束',  # 4
}

# db.conn()


def select_user(username):
    try:
        db.conn()
        sql = "select user_login_name as username,user_login_pwd as password from mis_user where user_login_name='{}';".format(username)
        results = db.select(sql)
    except Exception as e:
        print e
    return results



#更新项目信息
def update_project_by_projectid(manager_name,manager_member,pj_project_tracker_name,pj_action_expt,manager_type,pid):
    try:
        db.conn()
        sql = "UPDATE `kmedic_tab`.`project_info` SET `manager_name`='%s', `manager_member`='%s', " \
              "`pj_project_tracker_name`='%s', `pj_action_expt`='%s', `manager_type`='%s' " \
              " WHERE `id`='%s'" % (manager_name,manager_member,pj_project_tracker_name,pj_action_expt,manager_type,pid)

        results = db.dml(sql)
    except Exception as e:
        print e
    return results

#更新样本状态
def update_sample_by_projectid(sample_state,progress,sample_id):
    try:
        db.conn()
        if progress != 0:
            sql = "UPDATE `kmedic_tab`.`cq_sample` SET `state_info`='%s' ,`progress`='%s'  WHERE `id`='%s'" % (sample_state,progress,sample_id)
        else:
            sql = "UPDATE `kmedic_tab`.`cq_sample` SET `state_info`='%s' WHERE `id`='%s'" % (sample_state, sample_id)
        results = db.dml(sql)
    except Exception as e:
        print e
    return results

#更新报告文件
def update_sample_file(reported_file, sample_id):
    try:
        sql = "UPDATE `kmedic_tab`.`cq_sample` SET `reported_file`='%s' WHERE `id`='%s'" % (reported_file, sample_id)
        results = db.dml(sql)
    except Exception as e:
        print e
    return results

def update_project_state_by_projectid(manager_state_max,manager_state_min,manager_progress,pid):
    try:
        db.conn()
        sql = "UPDATE `kmedic_tab`.`project_info` SET `manager_state_max`='%s', `manager_state_min`='%s' , `manager_progress`='%s' WHERE `id`='%s'" \
              % (manager_state_max,manager_state_min,manager_progress,pid)
        results = db.dml(sql)
    except Exception as e:
        print e
    return results

#删除项目中的某个样本

def update_projectid_by_sampleid(cid,pid):
    try:
        db.conn()
        sql = "UPDATE `kmedic_tab`.`cq_sample` SET `project_id`='' WHERE `id`='%s' and `project_id`='%s'" % (cid,pid)
        results = db.dml(sql)
    except Exception as e:
        print e
    return results

#删除项目
def delete_project_by_id(pid):
    try:
        db.conn()
        sql = "DELETE FROM `kmedic_tab`.`project_info` WHERE `id`='%s';" % (pid)
        results = db.dml(sql)
    except Exception as e:
        print e
    return results

#根据项目ID取得所属样本最大状态和最小状态
def get_samples_maxstate_minstate(pid):
    try:
        db.conn()
        sql = "select max(state),min(state) from cq_sample where account_id = '%s';" % pid
        result = db.select(sql)
    except Exception as e:
        print e
    return result


#根据项目ID取得所属样本
def get_samples_by_projectid(pid):
    try:
        db.conn()
        sql_select = "select  id,sample_code,sample_type,state,progress,SYS_INSERTTIME from cq_sample where project_id='{}';".format(pid)
        results = db.select(sql_select)
    except Exception as e:
        print e
    return results


#根据项目ID取得项目
def get_project_by_id(sid):
    try:
        db.conn()
        sql_select = "select manager_name,manager_member,pj_project_tracker_name,pj_action_expt,manager_type ,manager_state_min, manager_state_max, id from project_info where id='{}';".format(sid)
        result = db.select(sql_select)
        if not result:
            result = u'无'
    except Exception as e:
        print e
    return result[0]

#取得样本
def get_sample_by_id(sid):
    try:
        db.conn()
        sql_select = "select * from cq_sample where id='{}';".format(sid)
        result = db.select(sql_select)
    except Exception as e:
        print e
    return result[0]

#取得样本实验数据
def get_inputinfo_by_sid(sid):
    try:
        db.conn()
        sql_select = "select * from info_input where sample_id='{}';".format(sid)
        result = db.select(sql_select)
    except Exception as e:
        print e
    return result

def update_samples_by_project_id(id,project_id):
    try:
        db.conn()
        sql = "UPDATE `kmedic_tab`.`cq_sample` SET `project_id`='%s' WHERE `id`='%s'" % (project_id, id)
        results = db.dml(sql)
    except Exception as e:
        print e
    return results
#取客户资料
def get_cilent_by_id(sid):
    try:
        db.conn()
        sql_select = "select * from cq_client where id='{}';".format(sid)
        result = db.select(sql_select)
    except Exception as e:
        print e
    return result[0]


def select_clientname_by_id(cid):
    try:
        db.conn()
        sql_select = "select * from cq_client where id='{}';".format(cid)
        result = db.select(sql_select)
    except Exception as e:
        print e
    return result[0]

#分页查询样本
def select_sample(sample_code=None,index=0,pagecount=5):
    try:
        db.conn()
        if sample_code is None or sample_code == '' or sample_code == 'None':
            sql_select = "select * from cq_sample order by sys_inserttime desc limit {},{};".format(index,pagecount)
            sql_select_count = "select count(*) from cq_sample order by sys_inserttime desc ;"
            count = db.select(sql_select_count)[0]['count(*)']
        else:
            sample_code = sample_code.encode('utf-8')
            sql_select = "select * from cq_sample where sample_code like '%{}%' order by sys_inserttime  desc limit {},{};".format(sample_code,index, pagecount)
            sql_select_count = "select count(*)  from cq_sample where sample_code like '%{}%' order by sys_inserttime desc ;".format(sample_code)
            count = db.select(sql_select_count)[0]['count(*)']
        results = db.select(sql_select)

        if count / float(pagecount) == count // pagecount:
            page = count // pagecount
        else:
            page = count // pagecount + 1
    except Exception as e:
        print "errors:" + str(e)
    return results,count,page

#分页查询样本
def select_sample_by_expcode(expcode=None,index=0,pagecount=5):
    try:
        db.conn()
        if expcode is None or expcode == '' or expcode == 'None':
            sql_select = "select * from cq_sample order by sys_inserttime desc limit {},{};".format(index,pagecount)
            sql_select_count = "select count(*) from cq_sample order by sys_inserttime desc ;"
            count = db.select(sql_select_count)[0]['count(*)']
        else:
            expcode = expcode.encode('utf-8')
            sql_select = "select distinct * from cq_sample as s1 , (( select sample_id from info_input where exp_number like '%{}%') as s2 )where s1.id = s2.sample_id limit {},{};".format(expcode,index, pagecount)
            sql_select_count = "select count(*) from (select distinct * from cq_sample as s1 , (( select sample_id from info_input where exp_number like '%{}%') as s2 )where s1.id = s2.sample_id) as s3;".format(expcode)
            count = db.select(sql_select_count)[0]['count(*)']
        results = db.select(sql_select)
        if count / float(pagecount) == count // pagecount:
            page = count // pagecount
        else:
            page = count // pagecount + 1
    except Exception as e:
        print "errors:" + str(e)
    return results,count,page


#分页查询项目
def select_project(manager_name=None,index=0,pagecount=5):
    #
    try:
        db.conn()
        if manager_name is None or manager_name == '' or manager_name == 'None':
            sql_select = "select * from project_info order by sys_inserttime and manager_progress desc limit {},{};".format(index,pagecount)
            sql_select_count = "select count(*) from project_info order by sys_inserttime desc ;"
            count = db.select(sql_select_count)[0]['count(*)']
        else:
            manager_name = manager_name.encode('utf-8')
            sql_select = "select * from project_info where manager_name like '%{}%' order by sys_inserttime and manager_progress desc limit {},{};".format(manager_name,index,
                                                                                                         pagecount)
            sql_select_count = "select count(*) from project_info where manager_name like '%{}%' order by sys_inserttime desc ;".format(manager_name)
            count = db.select(sql_select_count)[0]['count(*)']
        results = db.select(sql_select)
        if count / float(pagecount) == count // pagecount:
            page = count // pagecount
        else:
            page = count // pagecount + 1
    except Exception as e:
        print e
    #
    return results,count,page


#样本总数以及页数
def sample_count(pagecount=5):
    #
    try:
        db.conn()
        sql_select = "SELECT COUNT(*) FROM cq_sample ;"
        result = db.select(sql_select)[0]['COUNT(*)']
        if result / float(pagecount) == result // pagecount:
            page =  result // pagecount
        else:
            page =  result // pagecount + 1
    except Exception as e:
        print e
    return result,page


#项目总数以及页数
def project_count(pagecount=5):
    try:
        db.conn()
        sql_select = "SELECT COUNT(*) FROM project_info ;"
        result = db.select(sql_select)[0]['COUNT(*)']
        if result / float(pagecount) == result // pagecount:
            page =  result // pagecount
        else:
            page =  result // pagecount + 1
    except Exception as e:
        print e
    return result,page

#获取所有系统操作
def select_work_log():
    try:
        db.conn()
        sql_select = "select obj_id,log_excman,log_remark,log_time from k_workflow_obj_log order by log_time desc limit 8;"
        results = db.select(sql_select)
        for result in results:
            if result['obj_id'] is not None and result['obj_id'] != '':
                sql_select2 = "select ppoint_id,obj_yw_id from k_workflow_obj as k_workflow_obj where  id = '{}';".format(result['obj_id'] )
                flow = db.select(sql_select2)
                if flow:
                    if flow[0]['ppoint_id'] == '3575ef61-c4bf-43e3-9714-2d6338b2908c' or flow[0]['ppoint_id'] == 'd6c32cbc-88c9-443b-bacf-ab94f479a32b':
                        result['flow_type'] = u'项目'
                        sql_select3 = "select manager_name,manager_state_max from project_info where sample_id = '{}';".format(flow[0]['obj_yw_id'])
                        prohect = db.select(sql_select3)
                        result['flow_name'] = prohect[0]['manager_name']
                        result['flow_sate'] = prohect[0]['manager_state_max']
                        result['yw_man'] = ''
                    else:
                        result['flow_type'] = u'样本'
                        sql_select3 = "select sample_code,state,yw_man from cq_sample where id = '{}';".format(flow[0]['obj_yw_id'])
                        sample = db.select(sql_select3)
                        result['flow_name'] = sample[0]['sample_code']
                        result['flow_sate'] = sample[0]['state']
                        result['yw_man'] = sample[0]['yw_man']


            else:
                result['flow_type'] = u'系统'
                result['flow_name'] = u"用户操作"
                result['flow_sate'] = u'常规'
                result['yw_man'] = ''
    except Exception as e:
        print e

    return results


