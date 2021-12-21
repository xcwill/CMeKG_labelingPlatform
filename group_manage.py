from flask import Blueprint
from db import DB
import shutil
import datetime
import os,json,operator
from flask import Flask, render_template, request, make_response, send_file, send_from_directory, jsonify

group_manage_bp = Blueprint('group_manage', __name__)


@group_manage_bp.route('/')
def main():
    return '1'


@group_manage_bp.route('/get_groups', methods=['GET', 'POST'])
def get_groups():
    page = int(request.form.get('page'))
    cond = request.form.get('cond')

    groups = []
    gs = DB.query_all_groups()
    for g in gs:
        groups.append(g.group_name)
        # print(tas)

    groups = sorted(groups, reverse=False)

    if cond == '':
        if groups:
            if len(groups) % 11 == 0:
                page_total = len(groups) / 11
            else:
                page_total = int(len(groups) / 11) + 1
            if page == 1 and page_total == 1:
                return jsonify({'files': groups, 'page_total': page_total, 'data_length': len(groups), 'page_start': 1, 'page_end': len(groups)})
            elif page == page_total and page != 1:
                return jsonify({'files': groups[11 * (page-1):], 'page_total': page_total, 'data_length': len(groups),
                                'page_start': 11 * (page-1) + 1, 'page_end': len(groups)})
            else:
                return jsonify({'files': groups[11 * (page - 1): 11 * page], 'page_total': page_total, 'data_length': len(groups),
                                'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
        else:
            return 'no data'
    else:
        fils = []
        for g in groups:
            if cond in g:
                fils.append(g)
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


@group_manage_bp.route('/get_data_list', methods=['POST'])
def get_data_list():
    us = DB.query_all()
    ulist = []
    for u in us:
        ulist.append(u.username)
    name = request.form.get('name')
    if name != '':
        users = []
        us = DB.query_group_user_by_group_name(group_name=name)
        for u in us:
            users.append(u.username)
        return jsonify({'ulist': ulist, 'users': users})
    else:
        return jsonify({'ulist': ulist})


@group_manage_bp.route('/new_group', methods=['POST'])
def new_group():
    name = request.form.get('name')
    users = request.form.getlist('users[]')

    if DB.query_group_exist(group_name=name) is None:
        DB.add_new_group(group_name=name)
        if users:
            for u in users:
                if DB.query_group_user_exist(group_name=name, username=u) is None:
                    DB.add_group_user(group_name=name, username=u)
        return 'success'
    else:
        return '任务名已存在！'


@group_manage_bp.route('/upd_group', methods=['POST'])
def upd_task():
    name = request.form.get('name')
    new_name = request.form.get('new_name')
    users = request.form.getlist('users[]')
    us = request.form.getlist('us[]')
    if operator.eq(us, users) and name == new_name:
        return '无修改！'
    else:
        if new_name != name:
            DB.upd_group_name(group_name=name, new_name=new_name)
        for u in users:
            DB.del_group_user_by_group_name_username(group_name=name, username=u)
        for u in us:
            if name == new_name:
                DB.add_group_user(group_name=name, username=u)
            else:
                DB.add_group_user(group_name=new_name, username=u)
                DB.upd_task_group_name(group_name=name, new_name=new_name)
        return '修改成功！'


@group_manage_bp.route('/del_group', methods=['POST'])
def del_group():
    name = request.form.get('name')
    tasks = []
    ts = DB.query_task_group_exist_by_group_name(group_name=name)
    for t in ts:
        tasks.append(t.name)
    if tasks:
        return 'fail'
    else:
        DB.del_group_by_group_name(group_name=name)
        DB.del_task_group_by_group_name(group_name=name)
        DB.del_group_user_by_group_name(group_name=name)
        return 'success'

