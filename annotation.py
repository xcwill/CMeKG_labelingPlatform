from flask import Blueprint
from bs4 import BeautifulSoup as bs
import zipfile
from db import DB
import datetime
import os,json
from flask_login import current_user
from models import User
from flask import Flask, render_template, request, make_response, send_file, send_from_directory, jsonify

annotation_bp = Blueprint('annotation', __name__)


@annotation_bp.route('/<name>/<count>', methods=['POST', 'GET'])
def main(name, count):
    files = os.listdir('static/源文件/'+name + '/')
    firsts = os.listdir('static/一标/'+name + '/')
    seconds = os.listdir('static/二标/' + name + '/')
    three = os.listdir('static/三标/' + name + '/')
    files = sorted(files)
    firsts = sorted(firsts)
    seconds = sorted(seconds)
    three = sorted(three)
    username = current_user.username
    ens = []
    if os.path.exists('static/labels/' + username + '_en.txt'):
        with open('static/labels/' + username + '_en.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if line.strip().replace('\n', '') != '':
                    ens.append(line.strip().replace('\n', ''))
    else:
        with open('static/labels/' + username + '_en.txt', 'a') as f:
            pass
    res = []
    if os.path.exists('static/labels/' + username + '_re.json'):
        with open('static/labels/' + username + '_re.json', 'r', encoding='utf-8') as f:
            ex = json.load(f)
            if ex:
                for e in ex:
                    if e not in res:
                        res.append(e)
            rel_types = []
            for r in res:
                rel_type = r['e1_label'] + '-' + r['e2_label']
                if rel_type not in rel_types:
                    if rel_type == 'x-x':
                        rel_type = r['rel_type']
                    rel_types.append(rel_type)
            res_f = {}
            for rel in rel_types:
                if len(rel.split('-')) == 1:
                    e1_label = 'x'
                    e2_label = 'x'
                else:
                    e1_label = rel.split('-')[0]
                    e2_label = rel.split('-')[1]
                res_f[rel] = {
                    'rel_type': [],
                    'e1_label': e1_label,
                    'e2_label': e2_label
                }
                if len(rel.split('-')) == 1:
                    res_f[rel]['rel_type'].append(r['rel_type'])
                else:
                    for r in res:
                        if r['e1_label'] + '-' + r['e2_label'] == rel:
                            res_f[rel]['rel_type'].append(r['rel_type'])

    else:
        with open('static/labels/' + username + '_re.json', 'w', encoding='utf-8') as f:
            ex = []
            json.dump(ex, f, ensure_ascii=False)
    return render_template('annotation.html', nam=name, count=count, files=files, firsts=firsts, seconds=seconds, three=three, ens=ens, res_f=res_f)


@annotation_bp.route('/get_labels', methods=['POST'])
def get_labels():
    username = current_user.username
    ens = []
    if os.path.exists('static/labels/' + username + '_en.txt'):
        with open('static/labels/' + username + '_en.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if line != '':
                    ens.append(line.strip().replace('\n', ''))
    else:
        with open('static/labels/' + username + '_en.txt', 'a') as f:
            pass
    res = []
    if os.path.exists('static/labels/' + username + '_re.json'):
        with open('static/labels/' + username + '_re.json', 'r', encoding='utf-8') as f:
            export = json.load(f)
            if export:
                for e in export:
                    if e not in res:
                        res.append(e)
    else:
        with open('static/labels/' + username + '_re.json', 'w', encoding='utf-8') as f:
            export = []
            json.dump(export, f, ensure_ascii=False)
    return jsonify({'ens': ens, 'res': res})


@annotation_bp.route('/labels_config', methods=['POST'])
def labels_config():
    username = current_user.username
    ens = request.form.get('ens')
    res = request.form.get('res')
    es = []
    rs = []
    for en in ens.split('\n'):
        if en != '':
            es.append(en)
    try:
        with open('static/labels/' + username + '_en.txt', 'w', encoding='utf-8') as f:
            for e in es:
                f.write(e + '\n')
        for re in res.split('\n'):
            if re != '':
                rs.append(re)
        with open('static/labels/' + username + '_re.json', 'w', encoding='utf-8') as f:
            export = []
            for r in rs:
                xs = r.split()
                export.append({
                    'rel_type': xs[0],
                    'e1_label': xs[1],
                    'e2_label': xs[2]
                })
            json.dump(export, f, ensure_ascii=False)
            return 'success'
    except Exception:
        return 'error'


@annotation_bp.route('/get_file_content', methods=['POST'])
def get_file_content():
    name = request.form.get('name')
    filena = request.form.get('filena')
    save_path = request.form.get('save_path')
    if save_path == 'yuanwenjian':
        path = 'static/源文件/' + filena + '/' + name
    elif save_path == 'yibiao':
        path = 'static/一标/' + filena + '/' + name
    elif save_path == 'erbiao':
        path = 'static/二标/' + filena + '/' + name
    else:
        path = 'static/三标/' + filena + '/' + name
    ty = name.split('.')[-1]
    if ty != 'json':
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        data1 = {'content': content, 'content_new': content}
        return jsonify(data1)
    else:
        with open(path, 'r', encoding='utf-8') as f1:
            export = json.load(f1)
        result = export['result']
        data = result[0]
        content = data['content']
        spans = data['spans']
        spans = sorted(spans, key=lambda i: i['start_offset'], reverse=False)
        if 'relation' in data:
            relation = data['relation']
        else:
            relation = []
        if relation:
            relations = []
            for re in relation:
                r = {}
                r['label'] = re['rel_type']
                r['source'] = re['span_front']['start_offset']
                if 'en_property' not in re['span_front']:
                    r['en1_prop'] = ''
                else:
                    r['en1_prop'] = re['span_front']['en_property']
                r['target'] = re['span_after']['start_offset']
                if 'en_property' not in re['span_after']:
                    r['en2_prop'] = ''
                else:
                    r['en2_prop'] = re['span_after']['en_property']
                if 'rel_property' not in re:
                    r['rel_property'] = ''
                else:
                    r['rel_property'] = re['rel_property']
                relations.append(r)
                re_label = []
                re_labels = []
            # for re in relation:
            #     r = {}
            #     r['label'] = re['rel_type']
            #     r['start'] = re['span_front']['label']
            #     r['end'] = re['span_after']['label']
            #     re_label.append(r)
            # for re in re_label:
            #     if re not in re_labels:
            #         re_labels.append(re)
        else:
            re_labels = []
            relations = []
        if spans:
            before_start = 0
            content_new = ''
            global labels
            labels = []
            labs = []
            for span in spans:
                labs.append(span['label'])
            for lab in labs:
                if lab not in labels:
                    labels.append(lab)
            # print(labels)
           # print(spans)
            for span in spans:
                if span['label'] != 'null':
                    start = span['start_offset']
                    end = span['end_offset']
                    span_name = span['span_name']
                    label = span['label']
                    before_span = content[before_start:start]
                    color = 'tag-txt'+get_entity_color(label, labels)
                    b = "<b class='tag-txt " + color + "' id=" + str(start) + " data-start=" + str(start) + " data-end=" \
                        + str(end) + " data-char=" + span_name + " data-entity=" + label + ">" + span_name + "</b>"
                    content_new += before_span+b
                    before_start = end

            content_new += content[spans[-1]['end_offset']:]
            # print(content_new)
            # print(relations)
            data = {'content_new': content_new, 'relations': relations, 'content': content}
        else:
            data = {'content_new': content, 'relations': relations, 'content': content}
        return jsonify(data)


def get_entity_color(label,las):
    i = 0
    for la in las:
        if label == la:
            return str(i)
        i += 1


@annotation_bp.route('/to_json',methods=['POST'])
def to_json():
    export = {}
    result = []
    data = {}
    spans = []
    data1 = request.form.get('html')
    content = request.form.get('content')
    relations = request.form.get('relations')
    filena = request.form.get('filena')
    name = request.form.get('name')
    save_path = request.form.get('save_path')
    save = request.form.get('save')
    relation = json.loads(relations)
    soup = bs(data1, 'lxml')
    for b in soup.find_all('b'):
        span = {}
        span['span_name'] = b.get_text()
        span['label'] = b.get('data-entity')
        span['start_offset'] = int(b.get('data-start'))
        span['end_offset'] = int(b.get('data-end'))
        spans.append(span)
    sps = []
    for span in spans:
        # print(span)
        if span['start_offset'] > span['end_offset']:
            t = span['start_offset']
            span['start_offset'] = span['end_offset']
            span['end_offset'] = t
            sps.append(span)
        else:
            sps.append(span)
    # print(relation)
    for re in relation[::]:
        #re['rel_type'] = '并发症'
        if 'start_offset' in re['span_front'] and  'start_offset' in re['span_after']:
        #print(re)
            re['span_front']['start_offset'] = int(re['span_front']['start_offset'])
            re['span_front']['end_offset'] = int(re['span_front']['end_offset'])
            re['span_after']['start_offset'] = int(re['span_after']['start_offset'])
            re['span_after']['end_offset'] = int(re['span_after']['end_offset'])
        else:
            # print(re)
            relation.remove(re)
    # print(relation)
    # for re in relation[::]:
    #     if (re['span_front'] not in sps) or (re['span_after'] not in sps):
    #         relation.remove(re)
    # print(relation)
    data['data_id'] = 335623
    data['content'] = content
    data['spans'] = sps
    data['relation'] = relation
    result.append(data)
    export['result'] = result

    if save == 'no_save':
        if save_path == 'yuanwenjian':
            out = 'static/一标/' + filena + '/' + name + '.json'
        elif save_path == 'yibiao':
            out = 'static/二标/' + filena + '/' + name + '.json'
        elif save_path == 'erbiao':
            out = 'static/三标/' + filena + '/' + name + '.json'
        else:
            out = 'static/三标/' + filena + '/' + name + '.json'
    else:
        if save_path == 'yuanwenjian':
            out = 'static/一标/' + filena + '/' + name + '.json'
        elif save_path == 'yibiao':
            out = 'static/一标/' + filena + '/' + name + '.json'
        elif save_path == 'erbiao':
            out = 'static/二标/' + filena + '/' + name + '.json'
        elif save_path == 'sanbiao':
            out = 'static/三标/' + filena + '/' + name + '.json'
    with open(out, 'w', encoding='utf-8') as f1:
        json.dump(export, f1, ensure_ascii=False)
    return 'success'


@annotation_bp.route('/save_file_update/<filename>', methods=['POST','GET'])
def save_file_update(filename):
    files = os.listdir('static/源文件/'+filename)
    firsts = os.listdir('static/一标/'+filename)
    seconds = os.listdir('static/二标/' + filename)
    three = os.listdir('static/三标/' + filename)
    if os.path.exists('static/zip/' + filename):
        with zipfile.ZipFile('static/zip/' + filename + '/'+filename+'_一标.zip', 'w') as azip:
            root = os.getcwd()
            os.chdir('static/一标/'+ filename)
            for x in firsts:
                azip.write(x)
            os.chdir(root)
        with zipfile.ZipFile('static/zip/' + filename + '/'+filename+'_二标.zip', 'w') as azip1:
            root = os.getcwd()
            os.chdir('static/二标/' + filename)
            for x in seconds:
                azip1.write(x)
            os.chdir(root)
        with zipfile.ZipFile('static/zip/' + filename + '/'+filename+'_三标.zip', 'w') as azip2:
            root = os.getcwd()
            os.chdir('static/三标/' + filename)
            for x in three:
                azip2.write(x)
            os.chdir(root)
    else:
        os.makedirs('static/zip/' + filename)
        with zipfile.ZipFile('static/zip/' + filename + '/'+filename+'_一标.zip', 'w') as azip:
            root = os.getcwd()
            os.chdir('static/一标/'+ filename)
            for x in firsts:
                azip.write(x)
            os.chdir(root)
        with zipfile.ZipFile('static/zip/' + filename + '/'+filename+'_二标.zip', 'w') as azip1:
            root = os.getcwd()
            os.chdir('static/二标/' + filename)
            for x in seconds:
                azip1.write(x)
            os.chdir(root)
        with zipfile.ZipFile('static/zip/' + filename + '/'+filename+'_三标.zip', 'w') as azip2:
            root = os.getcwd()
            os.chdir('static/三标/' + filename)
            for x in three:
                azip2.write(x)
            os.chdir(root)

    files = sorted(files)
    firsts = sorted(firsts)
    seconds = sorted(seconds)
    three = sorted(three)
    data = {'files':files,'firsts':firsts,'seconds':seconds,'three':three}
    return jsonify(data)



