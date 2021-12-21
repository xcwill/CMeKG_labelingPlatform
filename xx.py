import json, os
global i
def get_label(relation, po):
    res = [
        {'re': '病因', 'e1': '疾病', 'e2': '社会学'}, {'re': '相关疾病', 'e1': '疾病', 'e2': '疾病'}, {'re': '转移部位', 'e1': '疾病', 'e2': '部位'},
        {'re': '外侵部位', 'e1': '疾病', 'e2': '部位'}, {'re': '发病部位', 'e1': '疾病', 'e2': '部位'}, {'re': '临床症状', 'e1': '疾病', 'e2': '症状'},
        {'re': '术后症状', 'e1': '疾病', 'e2': '症状'}, {'re': '治疗后症状', 'e1': '疾病', 'e2': '症状'}, {'re': '侵及周围组织转移的症状', 'e1': '疾病', 'e2': '症状'},
        {'re': '临床体征', 'e1': '疾病', 'e2': '症状'}, {'re': '辅助检查', 'e1': '疾病', 'e2': '检查'}, {'re': '影像学检查', 'e1': '疾病', 'e2': '检查'},
        {'re': '内窥镜检查', 'e1': '疾病', 'e2': '检查'}, {'re': '组织学检查', 'e1': '疾病', 'e2': '检查'}, {'re': '筛查', 'e1': '疾病', 'e2': '检查'},
        {'re': '实验室检查', 'e1': '疾病', 'e2': '检查'}, {'re': '鉴别诊断', 'e1': '疾病', 'e2': '疾病'}, {'re': '并发症', 'e1': '疾病', 'e2': '疾病'},
        {'re': '并发症（术后）', 'e1': '疾病', 'e2': '疾病'}, {'re': '并发症（药物）', 'e1': '疾病', 'e2': '疾病'}, {'re': '相关（转化）', 'e1': '疾病', 'e2': '疾病'},
        {'re': '相关（导致）', 'e1': '疾病', 'e2': '疾病'}, {'re': '相关（症状）', 'e1': '疾病', 'e2': '疾病'}, {'re': '病理分型', 'e1': '疾病', 'e2': '疾病'},
        {'re': '放射治疗', 'e1': '疾病', 'e2': '其他治疗'},{'re': '辅助治疗', 'e1': '疾病', 'e2': '其他治疗'},{'re': '化疗', 'e1': '疾病', 'e2': '其他治疗'},
        {'re': '手术治疗', 'e1': '疾病', 'e2': '手术治疗'},{'re': '药物治疗', 'e1': '疾病', 'e2': '药物'},{'re': '发病年龄', 'e1': '疾病', 'e2': '流行病学'},
        {'re': '发病性别倾向', 'e1': '疾病', 'e2': '流行病学'},{'re': '发病率', 'e1': '疾病', 'e2': '流行病学'},{'re': '死亡率', 'e1': '疾病', 'e2': '流行病学'},
        {'re': '多发群体', 'e1': '疾病', 'e2': '流行病学'},{'re': '多发地区', 'e1': '疾病', 'e2': '流行病学'},{'re': '多发季节', 'e1': '疾病', 'e2': '流行病学'},
        {'re': '潜伏期', 'e1': '疾病', 'e2': '流行病学'},{'re': '传播途径', 'e1': '疾病', 'e2': '流行病学'},{'re': '其他', 'e1': '疾病', 'e2': '流行病学'},
        {'re': '预后状况', 'e1': '疾病', 'e2': '预后'},{'re': '预后生存时间', 'e1': '疾病', 'e2': '预后'},{'re': '预后10年生存率', 'e1': '疾病', 'e2': '预后'},
        {'re': '预后5年生存率', 'e1': '疾病', 'e2': '预后'},{'re': '预后生存率', 'e1': '疾病', 'e2': '预后'},{'re': '就诊科室', 'e1': '疾病', 'e2': '其他'},
        {'re': '出院标准', 'e1': '疾病', 'e2': '其他'},{'re': '转移方式', 'e1': '疾病', 'e2': '其他'},{'re': '病因', 'e1': '疾病', 'e2': '社会学'},
        {'re': '风险评估因素', 'e1': '疾病', 'e2': '社会学'},{'re': '高危因素', 'e1': '疾病', 'e2': '社会学'},{'re': '病史', 'e1': '疾病', 'e2': '社会学'},
        {'re': '遗传因素', 'e1': '疾病', 'e2': '社会学'},{'re': '发病机制', 'e1': '疾病', 'e2': '社会学'},{'re': '病理生理', 'e1': '疾病', 'e2': '社会学'},
    ]
    label = ''
    for r in res:
        if r['re'] == relation:
            if po == 'e1':
                label = r['e1']
            else:
                label = r['e2']
    if label != '':
        return label
    else:
        return None


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f1:
        results = json.load(f1)
        for r in results:
            ens = []
            text = r['text']
            if r['triples']:
                for triple in r['triples']:
                    if get_label(triple['relation'], 'e1') is not None:
                        en = {
                            'text': text,
                            'start': triple['e1_start_pos'],
                            'end': triple['e1_end_pos'],
                            'label': get_label(triple['relation'], 'e1')
                        }
                        if en not in ens:
                            ens.append(en)
                    if get_label(triple['relation'], 'e2') is not None:
                        en = {
                            'text': text,
                            'start': triple['e2_start_pos'],
                            'end': triple['e2_end_pos'],
                            'label': get_label(triple['relation'], 'e2')
                        }
                        if en not in ens:
                            ens.append(en)
            if ens:
                global i
                i += 1
                with open('C:\\Users\\12504\\Desktop\\555\\' + str(i) + '.txt','w' , encoding='utf-8') as f:
                    f.write(ens[0]['text'])
                with open('C:\\Users\\12504\\Desktop\\555\\' + str(i) + '_label' +'.txt', 'w', encoding='utf-8') as f:
                    ens = sorted(ens, key=lambda j: j['start'], reverse=False)
                    for en in ens:
                        f.write(en['text'][en['start']: en['end']] + ' ' + str(en['start']) + ' ' + str(en['end']) + ' ' + en['label'] + '\n')


if __name__ == '__main__':
    i = 0
    for file in os.listdir('E:\\医疗知识图谱\\best_practice_106_new3\\'):
        read_file('E:\\医疗知识图谱\\best_practice_106_new3\\' + file)
