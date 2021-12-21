from flask import Blueprint
from db import DB
import datetime
import os,json
import zipfile
from flask import Flask, render_template, request, make_response, send_file, send_from_directory, jsonify

download_manage_bp = Blueprint('download_manage', __name__)


@download_manage_bp.route('/')
def main():
    return 'a'

@download_manage_bp.route('/get_data', methods=['POST'])
def get_data():
    page = int(request.form.get('page'))
    file_path = request.form.get('file_path')
    group = request.form.get('group')
    cond = request.form.get('cond')

    if file_path == '':
        return 'no data'
    elif file_path == '' and group == '':
        return 'no data'
    else:
        files = os.listdir('static/' + file_path + '/')
        files = sorted(files, reverse=False)
        if group == '':
            if cond == '':
                if len(files) % 11 == 0:
                    page_total = len(files) / 11
                else:
                    page_total = int(len(files) / 11) + 1
                if page == 1 and page_total == 1:
                    gen_zip(file_path, files)
                    return jsonify({'files': files, 'page_total': page_total, 'data_length': len(files), 'page_start': 1,
                                    'page_end': len(files)})
                elif page == page_total and page != 1:
                    gen_zip(file_path, files)
                    return jsonify({'files': files[11 * (page - 1):], 'page_total': page_total, 'data_length': len(files),
                                    'page_start': 11 * (page - 1) + 1, 'page_end': len(files)})
                else:
                    gen_zip(file_path, files)
                    return jsonify(
                        {'files': files[11 * (page - 1): 11 * page], 'page_total': page_total, 'data_length': len(files),
                         'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
            else:
                fils = []
                for file in files:
                    if cond in file:
                        fils.append(file)
                if fils:
                    if len(fils) % 11 == 0:
                        page_total = len(fils) / 11
                    else:
                        page_total = int(len(fils) / 11) + 1
                    if page == 1 and page_total == 1:
                        gen_zip(file_path, fils)
                        return jsonify(
                            {'files': fils, 'page_total': page_total, 'data_length': len(fils), 'page_start': 1,
                             'page_end': len(fils)})
                    elif page == page_total and page != 1:
                        gen_zip(file_path, fils)
                        return jsonify(
                            {'files': fils[11 * (page - 1):], 'page_total': page_total, 'data_length': len(fils),
                             'page_start': 11 * (page - 1) + 1, 'page_end': len(fils)})
                    else:
                        gen_zip(file_path, fils)
                        return jsonify({'files': fils[11 * (page - 1): 11 * page], 'page_total': page_total,
                                        'data_length': len(fils),
                                        'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                else:
                    return 'no data'
        elif group != '':
            if cond == '':
                fils = []
                for file in files:
                    if DB.query_task_group_exist(task_name=file, group_name=group) is not None:
                        fils.append(file)
                if fils:
                    if len(fils) % 11 == 0:
                        page_total = len(fils) / 11
                    else:
                        page_total = int(len(fils) / 11) + 1
                    if page == 1 and page_total == 1:
                        gen_zip(file_path, fils)
                        return jsonify(
                            {'files': fils, 'page_total': page_total, 'data_length': len(fils), 'page_start': 1,
                             'page_end': len(fils)})
                    elif page == page_total and page != 1:
                        gen_zip(file_path, fils)
                        return jsonify(
                            {'files': fils[11 * (page - 1):], 'page_total': page_total, 'data_length': len(fils),
                             'page_start': 11 * (page - 1) + 1, 'page_end': len(fils)})
                    else:
                        gen_zip(file_path, fils)
                        return jsonify({'files': fils[11 * (page - 1): 11 * page], 'page_total': page_total,
                                        'data_length': len(fils),
                                        'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                else:
                    return 'no data'
            else:
                fils = []
                for file in files:
                    if DB.query_task_group_exist(task_name=file, group_name=group) is not None and cond in file:
                        fils.append(file)
                if fils:
                    if len(fils) % 11 == 0:
                        page_total = len(fils) / 11
                    else:
                        page_total = int(len(fils) / 11) + 1
                    if page == 1 and page_total == 1:
                        gen_zip(file_path, fils)
                        return jsonify(
                            {'files': fils, 'page_total': page_total, 'data_length': len(fils), 'page_start': 1,
                             'page_end': len(fils)})
                    elif page == page_total and page != 1:
                        gen_zip(file_path, fils)
                        return jsonify(
                            {'files': fils[11 * (page - 1):], 'page_total': page_total, 'data_length': len(fils),
                             'page_start': 11 * (page - 1) + 1, 'page_end': len(fils)})
                    else:
                        gen_zip(file_path, fils)
                        return jsonify({'files': fils[11 * (page - 1): 11 * page], 'page_total': page_total,
                                        'data_length': len(fils),
                                        'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                else:
                    return 'no data'

@download_manage_bp.route('/get_groups', methods=['POST'])
def get_groups():
    groups = []
    gs = DB.query_all_groups()
    for g in gs:
        groups.append(g.group_name)

    return jsonify({'groups': groups})


@download_manage_bp.route('/download/<save_path>/<name>/<filename>', methods=['GET'])
def download(filename,save_path, name):
    return send_from_directory('static/'+save_path+'/'+name, filename, mimetype='application/json',as_attachment=True)


def gen_zip(file_path, files):
    with zipfile.ZipFile('static/zip/' + '数据导出' + '/数据导出.zip', 'w') as azip:
        root = os.getcwd()
        for f in files:
            fs = os.listdir('static/'+file_path+'/' + f)
            os.chdir('static/'+file_path)
            for s in fs:
                azip.write(f + '/'+s)
            os.chdir(root)
