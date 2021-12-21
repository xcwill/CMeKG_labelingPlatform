from flask import Blueprint
from db import DB
import datetime
import os,json
import zipfile
from flask import Flask, render_template, request, make_response, send_file, send_from_directory, jsonify
import functools

table_page_manage_bp = Blueprint('table_page_manage', __name__)


@functools.lru_cache(maxsize=128, typed=False)
@table_page_manage_bp.route('/get_table', methods=['POST'])
def get_data():
    page = int(request.form.get('page'))
    file_path = request.form.get('file_path')
    group = request.form.get('group')
    cond = request.form.get('cond')
    repeat = request.form.get('repeat')
    con = request.form.get('con')

    if file_path == '':
        return 'no data'
    elif file_path == '' and group == '':
        return 'no data'
    else:
        files = os.listdir('static/' + file_path + '/')
        files = sorted(files, reverse=False)
        if group == '':
            if cond == '':
                if repeat == '1':
                    all_relations = get_relations(file_path, files)
                    if len(all_relations) % 11 == 0:
                        page_total = len(all_relations) / 11
                    else:
                        page_total = int(len(all_relations) / 11) + 1
                    if page == 1 and page_total == 1:
                        return jsonify({'files': all_relations, 'page_total': page_total, 'data_length': len(all_relations), 'page_start': 1,
                                        'page_end': len(all_relations)})
                    elif page == page_total and page != 1:
                        return jsonify({'files': all_relations[11 * (page - 1):], 'page_total': page_total, 'data_length': len(all_relations),
                                        'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                    else:
                        return jsonify(
                            {'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total, 'data_length': len(all_relations),
                             'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                else:
                    all_relations = []
                    all_relation = get_relations(file_path, files)
                    for re in all_relation:
                        if all_relations:
                            flag = False
                            for r in all_relations:
                                if re['rel_name'] == r['rel_name'] and re['rel_type'] == r['rel_type'] and re['entity1'] == r['entity1'] and re['entity1_type'] == r['entity1_type'] and re['entity2'] == r['entity2'] and re['entity2_type'] == r['entity2_type'] and re['rel_property'] == r['rel_property']:
                                    flag = True
                            if not flag:
                                all_relations.append(re)
                        else:
                            all_relations.append(re)
                    if len(all_relations) % 11 == 0:
                        page_total = len(all_relations) / 11
                    else:
                        page_total = int(len(all_relations) / 11) + 1
                    if page == 1 and page_total == 1:
                        return jsonify(
                            {'files': all_relations, 'page_total': page_total, 'data_length': len(all_relations),
                             'page_start': 1,
                             'page_end': len(all_relations)})
                    elif page == page_total and page != 1:
                        return jsonify({'files': all_relations[11 * (page - 1):], 'page_total': page_total,
                                        'data_length': len(all_relations),
                                        'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                    else:
                        return jsonify(
                            {'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                             'data_length': len(all_relations),
                             'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
            else:
                if con == '按疾病名称':
                    fils = []
                    for file in files:
                        if cond in file:
                            fils.append(file)
                    if fils:
                        if repeat == '1':
                            all_relations = get_relations(file_path, fils)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total, 'data_length': len(all_relations), 'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1):], 'page_total': page_total, 'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify({'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                        else:
                            all_relations = []
                            all_relation = get_relations(file_path, fils)
                            for re in all_relation:
                                if all_relations:
                                    flag = False
                                    for r in all_relations:
                                        if re['rel_name'] == r['rel_name'] and re['rel_type'] == r['rel_type'] and re['entity1'] == r['entity1'] and re['entity1_type'] == r['entity1_type'] and re['entity2'] == r['entity2'] and re['entity2_type'] == r['entity2_type'] and re['rel_property'] == r['rel_property']:
                                            flag = True
                                    if not flag:
                                        all_relations.append(re)
                                else:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify({'files': all_relations[11 * (page - 1):], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                    else:
                        return 'no data'
                elif con == '按关系名称':
                    if files:
                        if repeat == '1':
                            all_relations = []
                            all_relation = get_relations(file_path, files)
                            for re in all_relation:
                                if cond in re['rel_name']:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total, 'data_length': len(all_relations), 'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1):], 'page_total': page_total, 'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify({'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                        else:
                            all_relations = []
                            all_relation = []
                            all_rels = get_relations(file_path, files)
                            for re in all_rels:
                                if all_relation:
                                    flag = False
                                    for r in all_relation:
                                        if re['rel_name'] == r['rel_name'] and re['rel_type'] == r['rel_type'] and re['entity1'] == r['entity1'] and re['entity1_type'] == r['entity1_type'] and re['entity2'] == r['entity2'] and re['entity2_type'] == r['entity2_type'] and re['rel_property'] == r['rel_property']:
                                            flag = True
                                    if not flag:
                                        all_relation.append(re)
                                else:
                                    all_relation.append(re)
                            for re in all_relation:
                                if cond in re['rel_name']:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify({'files': all_relations[11 * (page - 1):], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                    else:
                        return 'no data'
                elif con == '按子关系名称':
                    if files:
                        if repeat == '1':
                            all_relations = []
                            all_relation = get_relations(file_path, files)
                            for re in all_relation:
                                if cond in re['rel_type']:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total, 'data_length': len(all_relations), 'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1):], 'page_total': page_total, 'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify({'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                        else:
                            all_relations = []
                            all_relation = []
                            all_rels = get_relations(file_path, files)
                            for re in all_rels:
                                if all_relation:
                                    flag = False
                                    for r in all_relation:
                                        if re['rel_name'] == r['rel_name'] and re['rel_type'] == r['rel_type'] and re['entity1'] == r['entity1'] and re['entity1_type'] == r['entity1_type'] and re['entity2'] == r['entity2'] and re['entity2_type'] == r['entity2_type'] and re['rel_property'] == r['rel_property']:
                                            flag = True
                                    if not flag:
                                        all_relation.append(re)
                                else:
                                    all_relation.append(re)
                            for re in all_relation:
                                if cond in re['rel_type']:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify({'files': all_relations[11 * (page - 1):], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                    else:
                        return 'no data'
                elif con == '按实体类型':
                    if files:
                        if repeat == '1':
                            all_relations = []
                            all_relation = get_relations(file_path, files)
                            for re in all_relation:
                                if cond in re['entity1_type'] or cond in re['entity2_type']:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total, 'data_length': len(all_relations), 'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1):], 'page_total': page_total, 'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify({'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                        else:
                            all_relations = []
                            all_relation = []
                            all_rels = get_relations(file_path, files)
                            for re in all_rels:
                                if all_relation:
                                    flag = False
                                    for r in all_relation:
                                        if re['rel_name'] == r['rel_name'] and re['rel_type'] == r['rel_type'] and re['entity1'] == r['entity1'] and re['entity1_type'] == r['entity1_type'] and re['entity2'] == r['entity2'] and re['entity2_type'] == r['entity2_type'] and re['rel_property'] == r['rel_property']:
                                            flag = True
                                    if not flag:
                                        all_relation.append(re)
                                else:
                                    all_relation.append(re)
                            for re in all_relation:
                                if cond in re['entity1_type'] or cond in re['entity2_type']:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify({'files': all_relations[11 * (page - 1):], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                     'data_length': len(all_relations),
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
                    if repeat == '1':
                        all_relations = get_relations(file_path, fils)
                        if len(all_relations) % 11 == 0:
                            page_total = len(all_relations) / 11
                        else:
                            page_total = int(len(all_relations) / 11) + 1
                        if page == 1 and page_total == 1:
                            return jsonify(
                                {'files': all_relations, 'page_total': page_total, 'data_length': len(all_relations), 'page_start': 1,
                                 'page_end': len(all_relations)})
                        elif page == page_total and page != 1:
                            return jsonify(
                                {'files': all_relations[11 * (page - 1):], 'page_total': page_total, 'data_length': len(all_relations),
                                 'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                        else:
                            return jsonify({'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                            'data_length': len(all_relations),
                                            'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                    else:
                        all_relations = []
                        all_relation = get_relations(file_path, fils)
                        for re in all_relation:
                            if all_relations:
                                flag = False
                                for r in all_relations:
                                    if re['rel_name'] == r['rel_name'] and re['rel_type'] == r['rel_type'] and re[
                                        'entity1'] == r['entity1'] and re['entity1_type'] == r['entity1_type'] and re[
                                        'entity2'] == r['entity2'] and re['entity2_type'] == r['entity2_type'] and re[
                                        'rel_property'] == r['rel_property']:
                                        flag = True
                                if not flag:
                                    all_relations.append(re)
                            else:
                                all_relations.append(re)
                        if len(all_relations) % 11 == 0:
                            page_total = len(all_relations) / 11
                        else:
                            page_total = int(len(all_relations) / 11) + 1
                        if page == 1 and page_total == 1:
                            return jsonify(
                                {'files': all_relations, 'page_total': page_total, 'data_length': len(all_relations),
                                 'page_start': 1,
                                 'page_end': len(all_relations)})
                        elif page == page_total and page != 1:
                            return jsonify(
                                {'files': all_relations[11 * (page - 1):], 'page_total': page_total,
                                 'data_length': len(all_relations),
                                 'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                        else:
                            return jsonify(
                                {'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                 'data_length': len(all_relations),
                                 'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                else:
                    return 'no data'
            else:
                if con == '按疾病名称':
                    fils = []
                    for file in files:
                        if DB.query_task_group_exist(task_name=file, group_name=group) is not None and cond in file:
                            fils.append(file)
                    if fils:
                        if repeat == '1':
                            all_relations = get_relations(file_path, fils)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total, 'data_length': len(all_relations), 'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1):], 'page_total': page_total, 'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify({'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                        else:
                            all_relations = []
                            all_relation = get_relations(file_path, fils)
                            for re in all_relation:
                                if all_relations:
                                    flag = False
                                    for r in all_relations:
                                        if re['rel_name'] == r['rel_name'] and re['rel_type'] == r['rel_type'] and re[
                                            'entity1'] == r['entity1'] and re['entity1_type'] == r['entity1_type'] and \
                                                re['entity2'] == r['entity2'] and re['entity2_type'] == r[
                                            'entity2_type'] and re['rel_property'] == r['rel_property']:
                                            flag = True
                                    if not flag:
                                        all_relations.append(re)
                                else:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total,
                                     'data_length': len(all_relations), 'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1):], 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                    else:
                        return 'no data'
                elif con == '按关系名称':
                    fils = []
                    for file in files:
                        if DB.query_task_group_exist(task_name=file, group_name=group) is not None:
                            fils.append(file)
                    if fils:
                        if repeat == '1':
                            all_relations = []
                            all_relation = get_relations(file_path, fils)
                            for re in all_relation:
                                if cond in re['rel_name']:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total, 'data_length': len(all_relations), 'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1):], 'page_total': page_total, 'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify({'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                        else:
                            all_relations = []
                            all_relation = []
                            all_rels = get_relations(file_path, fils)
                            for re in all_rels:
                                if all_relation:
                                    flag = False
                                    for r in all_relation:
                                        if re['rel_name'] == r['rel_name'] and re['rel_type'] == r['rel_type'] and re['entity1'] == r['entity1'] and re['entity1_type'] == r['entity1_type'] and re['entity2'] == r['entity2'] and re['entity2_type'] == r['entity2_type'] and re['rel_property'] == r['rel_property']:
                                            flag = True
                                    if not flag:
                                        all_relation.append(re)
                                else:
                                    all_relation.append(re)
                            for re in all_relation:
                                if cond in re['rel_name']:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify({'files': all_relations[11 * (page - 1):], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                    else:
                        return 'no data'
                elif con == '按子关系名称':
                    fils = []
                    for file in files:
                        if DB.query_task_group_exist(task_name=file, group_name=group) is not None:
                            fils.append(file)
                    if fils:
                        if repeat == '1':
                            all_relations = []
                            all_relation = get_relations(file_path, fils)
                            for re in all_relation:
                                if cond in re['rel_type']:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total, 'data_length': len(all_relations), 'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1):], 'page_total': page_total, 'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify({'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                        else:
                            all_relations = []
                            all_relation = []
                            all_rels = get_relations(file_path, fils)
                            for re in all_rels:
                                if all_relation:
                                    flag = False
                                    for r in all_relation:
                                        if re['rel_name'] == r['rel_name'] and re['rel_type'] == r['rel_type'] and re['entity1'] == r['entity1'] and re['entity1_type'] == r['entity1_type'] and re['entity2'] == r['entity2'] and re['entity2_type'] == r['entity2_type'] and re['rel_property'] == r['rel_property']:
                                            flag = True
                                    if not flag:
                                        all_relation.append(re)
                                else:
                                    all_relation.append(re)
                            for re in all_relation:
                                if cond in re['rel_type']:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify({'files': all_relations[11 * (page - 1):], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                    else:
                        return 'no data'
                elif con == '按实体类型':
                    fils = []
                    for file in files:
                        if DB.query_task_group_exist(task_name=file, group_name=group) is not None:
                            fils.append(file)
                    if fils:
                        if repeat == '1':
                            all_relations = []
                            all_relation = get_relations(file_path, fils)
                            for re in all_relation:
                                if cond in re['entity1_type'] or cond in re['entity2_type']:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total, 'data_length': len(all_relations), 'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1):], 'page_total': page_total, 'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify({'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                        else:
                            all_relations = []
                            all_relation = []
                            all_rels = get_relations(file_path, fils)
                            for re in all_rels:
                                if all_relation:
                                    flag = False
                                    for r in all_relation:
                                        if re['rel_name'] == r['rel_name'] and re['rel_type'] == r['rel_type'] and re['entity1'] == r['entity1'] and re['entity1_type'] == r['entity1_type'] and re['entity2'] == r['entity2'] and re['entity2_type'] == r['entity2_type'] and re['rel_property'] == r['rel_property']:
                                            flag = True
                                    if not flag:
                                        all_relation.append(re)
                                else:
                                    all_relation.append(re)
                            for re in all_relation:
                                if cond in cond in re['entity1_type'] or cond in re['entity2_type']:
                                    all_relations.append(re)
                            if len(all_relations) % 11 == 0:
                                page_total = len(all_relations) / 11
                            else:
                                page_total = int(len(all_relations) / 11) + 1
                            if page == 1 and page_total == 1:
                                return jsonify(
                                    {'files': all_relations, 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 1,
                                     'page_end': len(all_relations)})
                            elif page == page_total and page != 1:
                                return jsonify({'files': all_relations[11 * (page - 1):], 'page_total': page_total,
                                                'data_length': len(all_relations),
                                                'page_start': 11 * (page - 1) + 1, 'page_end': len(all_relations)})
                            else:
                                return jsonify(
                                    {'files': all_relations[11 * (page - 1): 11 * page], 'page_total': page_total,
                                     'data_length': len(all_relations),
                                     'page_start': 11 * (page - 1) + 1, 'page_end': page * 11})
                    else:
                        return 'no data'


def get_relations(file_path, files):
    all_relation = []
    for file in files:
        fs = os.listdir('static/' + file_path + '/' + file + '/')
        if fs:
            for f in fs:
                with open('static/' + file_path + '/' + file + '/' + f, 'r', encoding='utf-8') as f1:
                    export = json.load(f1)
                    result = export['result']
                    data = result[0]
                    if 'relation' in data:
                        relation = data['relation']
                    else:
                        relation = []
                    if relation:
                        for re in relation:
                            rel = {
                                'disease': file,
                                'rel_name': re['span_front']['label'] + '-' + re['span_after']['label'],
                                'rel_type': re['rel_type'],
                                'entity1': re['span_front']['span_name'],
                                'entity1_type': re['span_front']['label'],
                                'entity2': re['span_after']['span_name'],
                                'entity2_type': re['span_after']['label'],
                                'rel_property': re['rel_property'],
                                'source': f
                            }
                            all_relation.append(rel)
    return all_relation
