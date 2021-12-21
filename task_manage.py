from flask import Blueprint
from db import DB
import shutil
import datetime
import os,json,operator
from flask import Flask, render_template, request, make_response, send_file, send_from_directory, jsonify

task_manage_bp = Blueprint('task_manage', __name__)


@task_manage_bp.route('/')
def main():
    return '1'


@task_manage_bp.route('/get_data_list', methods=['POST'])
def get_data_list():
    fs = DB.query_all_files()
    flist = []
    for f in fs:
        flist.append(f.name)
    gs = DB.query_all_groups()
    glist = []
    for g in gs:
        glist.append(g.group_name)
    name = request.form.get('name')
    if name != '':
        datas = []
        groups = []
        ds = DB.query_task_file_by_task(task_name=name)
        gs = DB.query_task_group_by_task_name(name=name)
        ty = DB.query_task_exist(name=name).type

        for d in ds:
            datas.append(d.file_name)
        for g in gs:
            groups.append(g.group_name)
        pr_1, pr_2, pr_3 = get_progess(name)
        if str(pr_1) != '0%':
            return jsonify({'flist': flist, 'glist': glist, 'datas': datas, 'groups': groups, 'type': ty, 'disable': '0'})
        else:
            return jsonify({'flist': flist, 'glist': glist, 'datas': datas, 'groups': groups, 'type': ty, 'disable': '1'})
    else:
        return jsonify({'flist': flist, 'glist': glist})


@task_manage_bp.route('/new_task', methods=['POST'])
def new_task():
    name = request.form.get('name')
    ty = request.form.get('type')
    time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    user = request.form.get('user')
    groups = request.form.getlist('groups[]')
    datas = request.form.getlist('datas[]')

    if DB.query_task_exist(name) is None:
        count = 0
        words = 0
        for d in datas:
            f = DB.query_file_by_name(name=d)
            count += int(f.count)
            words += int(f.words)
        DB.add_task(name=name, ty=ty, count=count, time=time, user=user, words=words)
        if groups:
            for g in groups:
                if DB.query_task_group_exist(task_name=name, group_name=g) is None:
                    DB.add_task_group(name=name, group_name=g)
        if datas:
            for d in datas:
                if DB.query_task_file_exist(task_name=name, file_name=d) is None:
                    DB.add_task_file(task_name=name, file_name=d)
        if os.path.exists('static/源文件/' + name) is not True:
            os.mkdir('static/源文件/' + name)
            os.mkdir('static/一标/' + name)
            os.mkdir('static/二标/' + name)
            os.mkdir('static/三标/' + name)
            for d in datas:
                for f in os.listdir('static/file/' + d +'/'):
                    if os.path.exists('static/源文件/' + name + '/' + f):
                        shutil.copy('static/file/' + d + '/' + f, 'static/源文件/' + name + '/' + d + '-' + f)
                    else:
                        shutil.copy('static/file/' + d +'/' + f, 'static/源文件/' + name + '/' + f)
        return 'success'
    else:
        return '任务名已存在！'


@task_manage_bp.route('/get_tasks', methods=['GET','POST'])
def get_tasks():
    page = int(request.form.get('page'))
    cond = request.form.get('cond')
    role = request.form.get('role')
    user = request.form.get('user')

    if role == '管理员':
        tasks = []
        ts = DB.query_all_tasks()
        for t in ts:
            first, second, third = get_progess(t.name)
            if first == 'fail':
                first = '0%'
            if second == 'fail':
                second = '0%'
            if third == 'fail':
                third = '0%'

            tasks.append({'name': t.name, 'type': t.type, 'count': t.count, 'time': t.time, 'user': t.user,
                          'words': t.words, 'first': first, 'second': second, 'third': third})
    else:
        tasks = []
        tas = []
        gs = DB.query_group_user_by_username(user)
        for g in gs:
            tts = DB.query_task_group_by_group_name(g.group_name)
            for t in tts:
                if t.name not in tas:
                    tas.append(t.name)
        # print(tas)
        for t in tas:
            ta = DB.query_task_by_name(name=t)
            first, second, third = get_progess(ta.name)
            if first == 'fail':
                first = '0%'
            if second == 'fail':
                second = '0%'
            if third == 'fail':
                third = '0%'
            tasks.append({'name': ta.name, 'type': ta.type, 'count': ta.count, 'time': ta.time, 'user': ta.user,
                          'words': ta.words, 'first': first, 'second': second, 'third': third})

    tasks = sorted(tasks, key=lambda i: i['name'], reverse=False)
    # print(tasks)

    if cond == '':
        if tasks:
            if len(tasks) % 11 == 0:
                page_total = len(tasks) / 11
            else:
                page_total = int(len(tasks) / 11) + 1
            if page == 1 and page_total == 1:
                return jsonify({'files': tasks, 'page_total': page_total, 'data_length': len(tasks), 'page_start': 1, 'page_end': len(tasks)})
            elif page == page_total and page != 1:
                return jsonify({'files': tasks[11 * (page-1):], 'page_total': page_total, 'data_length': len(tasks),
                                'page_start': 11 * (page-1) + 1, 'page_end': len(tasks)})
            else:
                return jsonify({'files': tasks[11 * (page - 1): 11 * page], 'page_total': page_total, 'data_length': len(tasks),
                                'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
        else:
            return 'no data'
    else:
        fils = []
        for t in tasks:
            if cond in t['name']:
                fils.append(t)
        if fils:
            if len(fils) % 11 == 0:
                page_total = len(fils) / 11
            else:
                page_total = int(len(fils) / 11) + 1
            if page == 1 and page_total == 1:
                return jsonify({'files': fils, 'page_total': page_total, 'data_length': len(fils), 'page_start': 1, 'page_end': len(fils)})
            elif page == page_total and page != 1:
                return jsonify({'files': fils[11 * (page-1):], 'page_total': page_total, 'data_length': len(fils),
                                'page_start': 11 * (page-1) + 1, 'page_end': len(fils)})
            else:
                return jsonify({'files': fils[11 * (page - 1): 11 * page], 'page_total': page_total, 'data_length': len(fils),
                                'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
        else:
            return 'no data'


@task_manage_bp.route('/del_task', methods=['POST'])
def del_task():
    name = request.form.get('name')
    DB.del_task_by_name(name=name)
    DB.del_task_file_by_task_name(name=name)
    DB.del_task_group_by_task_name(name=name)
    if os.path.exists('static/源文件/' + name):
        path0 = 'static/源文件/' + name
        for fi in os.listdir(path0 + '/'):
            os.remove(path0 + '/' + fi)
        os.rmdir(path0)
        path = 'static/一标/' + name
        for fi in os.listdir(path + '/'):
            os.remove(path + '/' + fi)
        os.rmdir(path)
        path1 = 'static/二标/' + name
        for fi in os.listdir(path1 + '/'):
            os.remove(path1 + '/' + fi)
        os.rmdir(path1)
        path2 = 'static/三标/' + name
        for fi in os.listdir(path2 + '/'):
            os.remove(path2 + '/' + fi)
        os.rmdir(path2)
    return 'success'


@task_manage_bp.route('/get_task_se', methods=['POST'])
def get_task_se():
    name = request.form.get('name')
    datas = []
    users = []
    ds = DB.query_task_file_by_task(task_name=name)
    us = DB.query_task_user_by_name(name=name)

    for d in ds:
        datas.append(d.file_name)
    for u in us:
        users.append(u.username)
    return jsonify({'datas': datas, 'users': users})


@task_manage_bp.route('/upd_task', methods=['POST'])
def upd_task():
    name = request.form.get('name')
    new_name = request.form.get('new_name')
    groups = request.form.getlist('groups[]')
    datas = request.form.getlist('datas[]')
    gs = request.form.getlist('gs[]')
    ds = request.form.getlist('ds[]')
    if operator.eq(gs, groups) and name == new_name and operator.eq(ds, datas):
        return '无修改！'
    else:
        if new_name != name:
            DB.upd_task_name(name, new_name)
            if os.path.exists('static/源文件/' + name) and os.path.exists('static/一标/' + name) and os.path.exists(
                    'static/二标/' + name) and os.path.exists('static/三标/' + name):
                root = os.getcwd()
                os.chdir('static/源文件/')
                os.rename(name, new_name)
                os.chdir(root)
                os.chdir('static/一标/')
                os.rename(name, new_name)
                os.chdir(root)
                os.chdir('static/二标/')
                os.rename(name, new_name)
                os.chdir(root)
                os.chdir('static/三标/')
                os.rename(name, new_name)
                os.chdir(root)
        for g in groups:
            DB.del_task_group_by_task_name_group_name(task_name=name, group_name=g)
        for g in gs:
            if name == new_name:
                DB.add_task_group(name=name, group_name=g)
            else:
                DB.add_task_group(name=new_name, group_name=g)
        for u in datas:
            DB.del_task_file_by_task_name_file_name(task_name=name, file_name=u)
        for u in ds:
            if name == new_name:
                DB.add_task_file(task_name=name, file_name=u)
            else:
                DB.add_task_file(task_name=new_name, file_name=u)
        if name == new_name:
            pr_1, pr_2, pr_3 = get_progess(name)
            if str(pr_1) == '0%':
                if os.path.exists('static/源文件/' + name):
                    path = 'static/源文件/' + name
                    for fi in os.listdir(path + '/'):
                        os.remove(path + '/' + fi)
                for d in ds:
                    for f in os.listdir('static/file/' + d + '/'):
                        if os.path.exists('static/源文件/' + name + '/' + f):
                            shutil.copy('static/file/' + d + '/' + f, 'static/源文件/' + name + '/' + d + '-' + f)
                        else:
                            shutil.copy('static/file/' + d + '/' + f, 'static/源文件/' + name + '/' + f)
        else:
            pr_1, pr_2, pr_3 = get_progess(new_name)
            if str(pr_1) == '0%':
                if os.path.exists('static/源文件/' + new_name):
                    path = 'static/源文件/' + new_name
                    for fi in os.listdir(path + '/'):
                        os.remove(path + '/' + fi)
                for d in ds:
                    for f in os.listdir('static/file/' + d + '/'):
                        if os.path.exists('static/源文件/' + new_name + '/' + f):
                            shutil.copy('static/file/' + d + '/' + f, 'static/源文件/' + new_name + '/' + d + '-' + f)
                        else:
                            shutil.copy('static/file/' + d + '/' + f, 'static/源文件/' + new_name + '/' + f)

        return '修改成功！'


def get_progess(l):
    if os.listdir('static/源文件/'+l+'/'):
        if os.path.exists('static/源文件/'+l+'/') and  os.path.exists('static/一标/'+l+'/')and os.path.exists('static/二标/' + l + '/') and os.path.exists('static/三标/' + l + '/'):
            li = os.listdir('static/源文件/'+l+'/')
            li1 = os.listdir('static/一标/'+l+'/')
            li2 = os.listdir('static/二标/' + l + '/')
            li3 = os.listdir('static/三标/' + l + '/')
            pr_1 = (len(li1)/len(li))
            pr_1 = format(pr_1, '.0%')
            pr_2 = (len(li2) / len(li))
            pr_2 = format(pr_2, '.0%')
            pr_3 = (len(li3) / len(li))
            pr_3 = format(pr_3, '.0%')

            return pr_1, pr_2, pr_3
        else:
            return 'fail'
    else:
        return 'fail'


