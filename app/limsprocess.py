#coding:utf8
# from runserver import app
from flask import render_template,request,jsonify,Response,flash,redirect,url_for
from limsMsql import *
from flask_login import login_required
from utils import query_user,User, workdays
from flask_login import login_user,logout_user
import hashlib
from werkzeug.utils import secure_filename
import os



from app import app


def get_sample_list(samples):
    samplelist = []
    for sample in samples:
        client = select_clientname_by_id(sample['cq_client_id'])
        should_report_time = workdays(start=sample['sample_re_time'], count=16).strftime('%Y-%m-%d')
        progress_tuple = ('信息录入', 'DNA提取', '文库构建', '上机测序', '检测结果', '生信分析', '生成报告', '报告发送', '结束')
        Pro = 0;
        #print 'zhungtai: ',sample['state_info']
        for i in range(len(progress_tuple)):
            if progress_tuple[i].decode('utf-8')==sample['state_info']:
                #print 'i: ', i
                Pro = (i+1)*100/len(progress_tuple)
        #print 'Pro: ', Pro
        samplelist.append({'id': sample['id'],
                           'sample_code': sample['sample_code'],
                           'sample_type': sample['sample_type'],
                           'sample_sjyy': sample['sample_sjyy'],
                           'AIM10': sample['AIM10'],
                           'state_info': sample['state_info'],
                           'reported_time': sample['reported_time'],
                           'state': sample['state'],
                           'sample_re_time': sample['sample_re_time'],
                           'progress': Pro,
                           'client_name': client['client_name'],
                           'should_report_time': should_report_time,
                           'exp_number' : client['h_dj_code'] or client['h_bl_code'],
                           'reported_file' : sample['reported_file'],
                           })
    return samplelist
#首页
@app.route('/')
@app.route('/index')
def index():
    samples,count,page = select_sample(index=0,pagecount=5)
    samplelist = get_sample_list(samples)
    worklogs = select_work_log()
    projects,count,page = select_project(index=0,pagecount=5)
    samplecount, page = sample_count(pagecount=5)
    projectcount, page = project_count(pagecount=5)
    user = select_user('admin')
    return render_template("index.html", title='Home', samples=samples, state_list=state_list, samplelist=samplelist,
                           worklogs=worklogs, projects=projects, project_state_list=project_state_list,
                           samplecount=samplecount, projectcount=projectcount)


# 所有样本
@app.route('/samples',methods=['GET','POST'])
@app.route('/samples/<int:pageindex>',methods=['GET','POST'])
def get_sample_page(pageindex=1, pagecount=100):
    if pageindex < 0 :
        pageindex = 0
    sample_code = request.form.get('search', None)
    search_by_expcode = request.form.get('search_by_expcode', None)
    if request.method == "POST":
        # print 1
        if sample_code is not None:
            samples, count, page = select_sample(sample_code=sample_code, index=(pageindex - 1) * pagecount,
                                                 pagecount=pagecount)

        elif search_by_expcode is not None:
            samples, count, page = select_sample_by_expcode(expcode=search_by_expcode, index=(pageindex - 1) * pagecount,
                                                            pagecount=pagecount)
        else:
            # print 3
            # samples, count, page = select_sample(sample_code=sample_code, index=(pageindex - 1) * pagecount,
            #                                      pagecount=pagecount)
            return render_template('index.html')

        samplelist = get_sample_list(samples)

        # print samplelist
        return render_template('samples.html', title='searching samples', samples=samples, count=count, page=page, samplelist=samplelist,
                               state_list=state_list, pageindex=pageindex, sample_code=sample_code)
    else:
        # print 2
        # samples, samplescount, samplespage = select_sample(sample_code=sample_code,index=(pageindex-1)*pagecount,pagecount=pagecount)
        # if sample_code is None or sample_code == '':
        #     count, page = sample_count(pagecount)
        # else:
        #     count, page = samplescount, samplespage
        # samplelist = get_sample_list(samples)
        #
        # # print samplelist
        #
        # return render_template('samples.html', title='Samples', samples=samples, count=count, page=page, state_list=state_list, pageindex=pageindex, samplelist=samplelist, sample_code=sample_code)

        return render_template('index.html')

#所有项目
# @app.route('/projects/<int:pageindex>',methods=['GET','POST'])
# def get_project_page(pageindex=1,pagecount=10):
#     if pageindex < 0 :
#         pageindex = 0
#     manager_name = request.args.get('search')
#     if request.method == "POST":
#         manager_name = request.form.get('search')
#         if manager_name is None or manager_name == '': sample_code = None
#         projects, count, page = select_project(manager_name=manager_name, index=(pageindex - 1) * pagecount,
#                                                pagecount=pagecount)
#
#         return render_template('samples.html', title='searching projects', projects=projects, count=count, page=page,
#                                state_list=state_list, pageindex=pageindex, manager_name=manager_name)
#     else:
#         projects, projectcount, projectpage = select_project(manager_name=manager_name, index=(pageindex - 1) * pagecount,
#                                                              pagecount=pagecount)
#         if manager_name is None or manager_name == '':
#             count, page = project_count(pagecount)
#         else:
#             count, page = projectcount, projectpage
#
#
#     return render_template('projects.html', title='Projects', projects=projects, count=count, page=page, project_state_list=project_state_list, pageindex=pageindex, manager_name=manager_name)


#样本详情
@app.route('/sampledetail/<string:sample_id>')
def get_sample_detail(sample_id):
    sample = get_sample_by_id(sample_id)
    client = get_cilent_by_id(sample['cq_client_id'])
    project = get_project_by_id(sample['account_id'])
    sample_inputinfo = get_inputinfo_by_sid(sample_id)
    return render_template('sampledetail.html', title='sample_details:{}'.format(sample['sample_code']), sample=sample, client=client, state_list=state_list,
                           project=project,sample_inputinfo=sample_inputinfo
                           )


#项目详情
@app.route('/projectdetail/<string:project_id>')
def get_project_detail(project_id):
    project = get_project_by_id(project_id)
    samples = get_samples_by_projectid(project['id'])
    return render_template('projectdetail.html', title='project_details:%s' % project['manager_name'], project=project, project_state_list=project_state_list,
                           samples=samples, state_list=state_list)



#修改项目相关资料
@login_required
@app.route('/projectmodify/<string:project_id>',methods=['GET','POST'])
def get_project_modify(project_id):
    project = get_project_by_id(project_id)
    if request.method == 'POST':
        manager_name = request.form.get('manager_name')
        pj_project_tracker_name = request.form.get('pj_project_tracker_name')
        pj_action_expt = request.form.get('pj_action_expt')
        manager_member = request.form.get('manager_member')
        manager_type = request.form.get('manager_type')
        try:
            update_project_by_projectid(manager_name,manager_member,pj_project_tracker_name,pj_action_expt,manager_type,project_id)
        except Exception as e:
            return jsonify(errors="can't update the data,please contract  administrator.")
        return jsonify(manager_name=manager_name,manager_member=manager_member,pj_project_tracker_name=pj_project_tracker_name, pj_action_expt=pj_action_expt, manager_type=manager_type,)

    samples = get_samples_by_projectid(project['id'])

    return render_template('projectmodify.html', title='project_details:%s' % project['manager_name'], project=project, project_state_list=project_state_list,
                           samples=samples, state_list=state_list)


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


#修改样本状态
@login_required
@app.route('/samplestate/<string:sample_id>',methods=['GET','POST'])
def get_sample_modify(sample_id):
    sample = get_sample_by_id(sample_id)
    if request.method == 'POST':
        sample_state = request.form.get('sample_state')
        progress = 0
        try:
            # if int(sample_state) == 0: progress = 16  # 收样登记
            # if int(sample_state) == 1: progress = 32  # 收样审核
            # if int(sample_state) == 2: progress = 48  # 信息录入
            # if int(sample_state) == 3: progress = 64  # 检测审核
            # if int(sample_state) == 4: progress = 80  # 生成报告
            # if int(sample_state) == 5: progress = 95  # 报告发送
            # if int(sample_state) == 6: progress = 100  # 结束
            # if int(sample_state) == -1: progress = 16  # 批量登记
            # if int(sample_state) == -2: progress = 32  # 批量审核

            # 状态补充
            if sample['state'] >= 2 and sample['state'] <= 3:
                if num(sample_state) == 2:
                    progress = 64




            update_sample_by_projectid(state_list[num(sample_state)],progress,sample_id)

        except Exception as e:
            return jsonify(errors="can't update the data,please contract  administrator.")
        sample_state_text = state_list[num(sample_state)]
        return jsonify(sample_state_text=sample_state_text)

    return render_template('samplestatetmodify.html', state_list=state_list, sample=sample)


#修改项目所有的样本
@login_required
@app.route('/updatesamples',methods=['GET','POST'])
def update_project_samples():
    if request.method == 'POST':
        project_id = request.args.get('project_id')
        sample_ids = request.form.get('sample_id')
        if not sample_ids:
            return jsonify(errors="没有选择任何样本.")
        sampleids = sample_ids.split(",")
        for sample_id in sampleids[:-1]:
            try:
                update_samples_by_project_id(sample_id,project_id)
            except Exception as e:
                return jsonify(errors="can't update the data id: %s,please contract  administrator." % sample_id)
        samples = get_samples_by_projectid(project_id)
        project = get_project_by_id(project_id)
        sample_state = []
        if samples:
            for sample in samples:
                sample_state.append(sample['state'])
            project_sample_state_max = max(sample_state)
            project_sample_state_min = min(sample_state)
            project_progress = 0
            for i in range(len(samples)):
                project_progress = project_progress + samples[i]['progress']
            project_progress = project_progress / len(samples)
        else:
            project_sample_state_max = 0
            project_sample_state_min = 0
            project_progress = 0
        try:
            update_project_state_by_projectid(project_sample_state_max, project_sample_state_min, project_progress,project_id)
        except Exception as e:
            return jsonify(errors="can't update the data,please contract  administrator.")
        return jsonify(samples=samples,project=project,state_list=state_list)


#删除项目拥有的样本
@login_required
@app.route('/deletesamples',methods=['GET','POST'])
def delete_project_sample():
    if request.method == 'POST':
        project_id = request.args.get('project_id')
        sample_id = request.args.get('sample_id')
        try:
            update_projectid_by_sampleid(sample_id, project_id)
        except Exception as e:
            return jsonify(msg="can't update the data id: %s,please contract  administrator." % sample_id)
        samples = get_samples_by_projectid(project_id)
        project = get_project_by_id(project_id)
        sample_state = []
        if samples:
            for sample in samples:
                sample_state.append(sample['state'])
            project_sample_state_max = max(sample_state)
            project_sample_state_min = min(sample_state)
            project_progress = 0
            for i in range(len(samples)):
                project_progress = project_progress + samples[i]['progress']
            project_progress = project_progress / len(samples)
        else:
            project_sample_state_max = 0
            project_sample_state_min = 0
            project_progress = 0
        try:
            update_project_state_by_projectid(project_sample_state_max, project_sample_state_min, project_progress,
                                              project_id)
        except Exception as e:
            return jsonify(msg="can't update the data,please contract  administrator.")
        return jsonify(samples=samples, project=project, state_list=state_list,success=True,mess='你已经删除样本!')

# 删除项目
@login_required
@app.route('/deleteproject', methods=['GET', 'POST'])
def delete_project():
    if request.method == 'POST':
        project_id = request.args.get('project_id')
        try:
            samples = get_samples_by_projectid(project_id)
            # project = get_project_by_id(project_id)
        except Exception as e:
            return jsonify(errors="can't update the project ,please contract  administrator." )
        if samples:
            return jsonify(errors="can't update the project ,该项目下仍有多个样本,非空项目,无法删除.")
        else:
            try:
                delete_project_by_id(project_id)
            except Exception as e:
                return jsonify(errors="can't update the project ,please contract  administrator." )
            return jsonify(success=True,mess=u"成功删除该项目")



#选择样本进项目
@app.route('/selectsamples',methods=['GET','POST'])
@app.route('/selectsamples/<int:pageindex>',methods=['GET','POST'])
@login_required
def get_sample_select_to_project(pageindex=1,pagecount=50):
    if pageindex < 0:
        pageindex = 0
    sample_code = request.args.get('search')
    project_id = request.args.get('project_id')
    if request.method == "POST":
        sample_code = request.form.get('search')
        if sample_code is None or sample_code == '': sample_code = None
        samples, count, page = select_sample(sample_code=sample_code, index=(pageindex - 1) * pagecount,
                                             pagecount=pagecount)

        return render_template('selectsampletoproject.html', title='searching samples', samples=samples, count=count, page=page,
                               state_list=state_list, pageindex=pageindex, sample_code=sample_code, project_id=project_id)
    else:
        samples, samplescount, samplespage = select_sample(sample_code=sample_code, index=(pageindex - 1) * pagecount,
                                                           pagecount=pagecount)
        if sample_code is None or sample_code == '':
            count, page = sample_count(pagecount)
        else:
            count, page = samplescount, samplespage
        return render_template('selectsampletoproject.html', title='Samples', samples=samples, count=count, page=page,
                               state_list=state_list, pageindex=pageindex, sample_code=sample_code, project_id=project_id)



#简易登陆登出功能
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        user = query_user(username)
        # 验证表单中提交的用户名和密码
        if user is not None and hashlib.md5(request.form['password']).hexdigest()[:16].upper() == user['password']:
            curr_user = User()
            curr_user.id = username

            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user)

            # 如果请求中有next参数，则重定向到其指定的地址，
            # 没有next参数，则重定向到"index"视图
            return jsonify(success=True, username=username)
        flash('Wrong username or password!')
    # GET 请求
    return render_template('login.html')


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/createproject/',methods=['GET', 'POST'])
@login_required
def createproject():
    from postrequest import lims_login,post_project
    sess = lims_login("admin","admin123456")
    state_code = post_project(sess)
    if state_code == 200 :
        return jsonify(success=True)
    else:
        return jsonify(error=True)


from flask import send_file
base_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = base_dir + '/upload/'

@login_required
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


@login_required
@app.route('/upload_file/<string:sample_id>', methods=['GET', 'POST'])
def upload_file(sample_id):

    if request.method == 'POST':
        # sample_id = request.form.get('sample_id')
        sample = get_sample_by_id(sample_id)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        uploaddir = os.path.join(UPLOAD_FOLDER, '%s/' % sample['sample_code'])
        if not os.path.exists(uploaddir):
            os.makedirs(uploaddir)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(uploaddir, filename))
            update_sample_file(os.path.join('%s/' % sample['sample_code'], filename), sample_id)
        return redirect(url_for('get_sample_detail',
                                sample_id=sample_id))
    return redirect(url_for('get_sample_detail',
                            sample_id=sample_id))


@app.route('/return-files/')
def return_files():
    sample_file = request.args.get('reported_file')
    file_name = sample_file.split('/')[-1]
    file = os.path.join(UPLOAD_FOLDER, '%s' % sample_file)
    try:
        return send_file(file,
                         attachment_filename=file_name)
    except Exception as e:
        return str(e)

# b = True
# while (b):
#     try:
#         app.run()
#         login_manager = LoginManager()
#         login_manager.init_app(app)
#
#         b = False
#     except:
#         k = 0


