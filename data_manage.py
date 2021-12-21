from flask import Blueprint
from db import DB
import datetime
import os,json
from flask import Flask, render_template, request, make_response, send_file, send_from_directory, jsonify

data_manage_bp = Blueprint('data_manage', __name__)


@data_manage_bp.route('/')
def main():
    return '1'


@data_manage_bp.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file')
        dataname = request.form.get('dataname')
        if os.path.exists('static/file/'+dataname):
            return 'repeat'
        else:
            if files:
                os.makedirs('static/file/' + dataname)
                for file in files:
                    file.save('static/file/'+dataname+'/'+file.filename)
                time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
                ty = files[0].filename.split('.')[-1]
                words = get_words(dataname, ty)
                DB.add_file(name=dataname, type=ty, count=len(files), time=time,
                            user='admin', words=words)
                return 'success'
            else:
                return 'fail'


def get_words(dataname, ty):
    files = os.listdir('static/file/'+dataname + '/')
    count = 0
    for file in files:
        if ty == 'json':
            with open('static/file/'+dataname + '/' + file, 'r', encoding='utf-8') as f1:
                export = json.load(f1)
            result = export['result']
            data = result[0]
            content = data['content']
            content = content.replace('\n', '').replace(' ', '').replace('，', '').replace('。', '')
            count += len(content)
        else:
            with open('static/file/'+dataname + '/' + file, 'r', encoding='utf-8') as f:
                count += len(f.read().replace('\n', '').replace(' ', '').replace('，', '').replace('。', ''))
    return str(count)


@data_manage_bp.route('/get_files', methods=['POST'])
def get_files():
    files = []
    fs = DB.query_all_files()
    for f in fs:
        files.append({'name': f.name, 'type': f.type, 'count': f.count, 'time': f.time, 'user': f.user,
                      'words': f.words})
    page = int(request.form.get('page'))
    cond = request.form.get('cond')
    print(cond)
    files = sorted(files, key=lambda i: i['name'], reverse=False)
    if cond == '':
        if files:
            if len(files) % 11 == 0:
                page_total = len(files) / 11
            else:
                page_total = int(len(files) / 11) + 1
            if page == 1 and page_total == 1:
                return jsonify({'files': files, 'page_total': page_total, 'data_length': len(files), 'page_start': 1, 'page_end': len(files)})
            elif page == page_total and page != 1:
                return jsonify({'files': files[11 * (page-1):], 'page_total': page_total, 'data_length': len(files),
                                'page_start': 11 * (page-1) + 1, 'page_end': len(files)})
            else:
                return jsonify({'files': files[11 * (page - 1): 11 * page], 'page_total': page_total, 'data_length': len(files),
                                'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
        else:
            return 'no data'
    else:
        fils = []
        for file in files:
            if cond in file['name']:
                fils.append(file)
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


@data_manage_bp.route('/del_data', methods=['POST'])
def del_data():
    name = request.form.get('name')
    datas = []
    ds = DB.query_task_file_exist_by_file_name(name)
    for d in ds:
        datas.append(d.file_name)
    if datas:
        return 'fail'
    else:
        DB.del_task_file_by_file_name(file_name=name)
        DB.del_file_by_file_name(name=name)

        if os.path.exists('static/file/' + name):
            path0 = 'static/file/' + name
            for fi in os.listdir(path0 + '/'):
                os.remove(path0 + '/' + fi)
            os.rmdir(path0)
        return 'success'

@data_manage_bp.route('/new_name', methods=['POST'])
def new_name():
    name = request.form.get('name')
    new_name = request.form.get('new_name')
    DB.upd_file_name(name=name, new_name=new_name)
    DB.upd_task_file_by_file_name(file_name=name, new_name=new_name)
    root = os.getcwd()
    os.chdir('static/file/')
    os.rename(name, new_name)
    os.chdir(root)

    return 'success'






