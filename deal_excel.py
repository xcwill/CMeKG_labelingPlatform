import xlrd, re,csv,json,os
from collections import Counter

x = []
zzz = []
yyy = []
all = []
comp = []
mmm = []
def read_excel(path, sheet_name):
    with xlrd.open_workbook(path) as excel:
        sheet = excel.sheet_by_name(sheet_name)
        for i in range(1, sheet.nrows):
            a = sheet.cell(i, 5).value
            for p in a.split():
                mmm.append(p)
            strinf = re.compile('([0-9][.、])')
            y = ''
            for s in strinf.sub('|', a.replace('F1.', 'F1#').replace('F1、', 'F1*')).replace('；', '').replace('。', '').replace(';', '').replace('.', '').split('|'):
                xxx = re.compile('(孕[0-9]+)')
                lll = re.compile('([0-9]周)')
                ppp = re.compile('(产[0-9]产[0-9])')
                ppp1 = re.compile('(孕[0-9]产[0-9])')
                ppp2 = re.compile('(孕[ 0-9]产[ 0-9])')
                # and not re.findall('\?', s) and not re.findall('？', s)
                if not re.findall(xxx, s) and not re.findall(lll, s) and not re.findall(ppp, s) and not re.findall(ppp1, s) and not re.findall(ppp2, s):
                    # if not re.findall('\?', s) and not re.findall('？', s):
                    # for com in comp:
                    #     if s in com.keys():
                    #         print(s)
                    #         s = com[s]
                    #         print(s)
                    # print(s)
                    if s != '':
                        s = s.replace('；', '').replace('。', '').replace(';', '').replace('、', '').replace('.', '').replace(',', '').replace('，', '').replace('F1*', 'F1、').replace('F1#', 'F1.').replace(' ', '').replace('常1', '常').replace('血1', '血').replace('宫1', '宫').replace('迫1', '迫').replace('产2', '产').strip()
                        if len(re.findall('[0-9]', s)) == 1 and re.findall('[0-9]', s[:1]):
                            sttr = re.compile('[0-9]')
                            s = sttr.sub('', s)
                        if len(s) >= 1:
                            if s[-1] == '1':
                                s = s[:-1]
                        y += s + '|'
                        zzz.append(s.replace('?', '').replace('？', ''))
                    # else:
                    #     zzz.append(s.replace('?', '').replace('？', ''))
            x.append(y[:-1].strip())
        print(x)
    with open('C:\\Users\\12504\\Desktop\\19889.txt', 'a', encoding='utf-8') as f:
        con = Counter(zzz)
        for i in x:
            oo = ''
            for j in i.split('|'):
                # if con[j] >= 10:
                oo += j + ' '
            f.write(oo.strip() + '\n')
        print(len(x))
    # # # print(zzz)
    # with open('C:\\Users\\12504\\Desktop\\19889_不确定诊断电子病历（3816）诊断标签频次统计.txt', 'a', encoding='utf-8') as f:
    #     f.write('标签总数：' + str(len(zzz)) + '\n')
    #     print(Counter(zzz))
    #     count = 0
    #     for k, v in sorted(Counter(zzz).items(), key=lambda item: item[1], reverse=True):
    #         print(k, v)
    #         f.write(k + ':' + str(v) + '\n')
    #         count += v
    #     print(count)
def read_ex(path, sheet_name):
    with xlrd.open_workbook(path) as excel:
        sheet = excel.sheet_by_name(sheet_name)
        for i in range(1, sheet.nrows):
            a = sheet.cell(i, 5).value
            # b = sheet.cell(i, 6).value
            xi = ''
            for y in a.split()[1:]:
                if not re.findall('\?', y) and not re.findall('？', y):
                    xi += y + ' '
                    yyy.append(y)
                else:
                    yyy.append(y.replace('?', '').replace('？', ''))
            # if len(xi.strip().split()) == len(b.split()[1:]):
            #     li1 = xi.strip().split()
            #     li2 = b.split()[1:]
            #     for i in range(len(li1)):
            #         rx = {}
            #         if li1[i] != li2[i]:
            #             rx[li1[i]] = li2[i]
            #             if rx not in comp:
            #                 comp.append(rx)
        # with open('C:\\Users\\12504\\Desktop\\labels.json', 'w', encoding='utf-8') as f1:
        #     json.dump(comp, f1, ensure_ascii=False)

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f1:
        export = json.load(f1)
    result = export['result']
    data = result[0]
    # content = data['content']
    #     # spans = data['spans']
    #     # relation = data['relation']
    return data


if __name__ == '__main__':

    # read_excel('C:\\Users\\12504\\Desktop\\19889数据集中确定诊断电子标签（15656）.xlsx', '确定诊断电子标签（15656）')
    # print(len(zzz))
    # read_excel('C:\\Users\\12504\\Desktop\\19889原始数据集结构化及处理0409.xlsx', '确定诊断电子病历（15658）')
    # print(zzz)
    # print(len(zzz))
    # read_ex('C:\\Users\\12504\\Desktop\\电子病历结构化原始结果及标签删减规范处理.xlsx', '原始电子病历及规范化标签')
    # print(yyy)
    # print(len(yyy))
    # with open('C:\\Users\\12504\\Desktop\\labels.json', 'r', encoding='utf-8') as f1:
    #     comp = json.load(f1)
    # print(len(comp))
    # print(comp)
    # read_excel('C:\\Users\\12504\\Desktop\\19889原始数据集20190405_已处理.xlsx', 'Sheet')

    # print(len(zzz))
    # print(zzz)
    # print(len(yyy))
    # print(yyy)

    # print(len(all))
    # con1 = Counter(yyy)
    # con2 = Counter(zzz)
    # print(len(con1))
    # print(len(con2))
    # result = []
    # for a in all:
    #     res = {}
    #     res['label'] = a
    #     if a in yyy:
    #         res['con1'] = con1[a]
    #     else:
    #         res['con1'] = 0
    #     if a in zzz:
    #         res['con2'] = con2[a]
    #     else:
    #         res['con2'] = 0
    #     result.append(res)
    # print(result)
    # for z in zzz:
    #     if z not in all:
    #         all.append(z)
    # for y in yyy:
    #     if y not in all:
    #         all.append(y)
    # print(len(all))
    # con1 = Counter(yyy)
    # con2 = Counter(zzz)
    # print(len(con1))
    # print(len(con2))
    # result = []
    # for a in all:
    #     res = {}
    #     res['label'] = a
    #     if a in yyy:
    #         res['con1'] = con1[a]
    #     else:
    #         res['con1'] = 0
    #     if a in zzz:
    #         res['con2'] = con2[a]
    #     else:
    #         res['con2'] = 0
    #     result.append(res)
    # print(result)
    # with open('C:\\Users\\12504\\Desktop\\10866_19889_删减后诊断标签比较0409.csv', 'w', newline='', encoding='utf-8')as f:
    #     write = csv.writer(f, dialect='excel')
    #     for re in result:
    #         line = [re['label'], re['con1'], re['con2']]
    #         write.writerow(line)
    relations = []
    relations_norepeat = []
    labels = []
    pp = '儿科学'
    with open('C:\\Users\\12504\\Desktop\\儿科学关系导出0512_' + pp + '.csv', 'a', newline='', encoding='utf-8')as f:
        write = csv.writer(f, dialect='excel')
        for p in os.listdir('C:\\Users\\12504\\Desktop\\' + pp + '\\'):
            for pa in os.listdir('C:\\Users\\12504\\Desktop\\' + pp + '\\' + p + '\\'):
                if pa.split('.')[-1] == 'json':
                    data = read_json('C:\\Users\\12504\\Desktop\\' + pp + '\\' + p + '\\' + pa)
                    spans = data['spans']
                    for span in spans:
                        if span['label'] == '药物治疗':
                            span['label'] = '药物'
                    for span in spans:
                        xx = {
                            'span_name': span['span_name'],
                            'label': span['label']
                        }
                        if span['label'] not in labels:
                            if span['label'] != '' and span['label'] != 'null' and span['label'] is not None:
                                labels.append(span['label'])
                        if xx['label'] != '' and xx['label'] != 'null' and xx['label'] is not None:
                            relations.append(xx)
                        if xx['label'] != '' and xx['label'] != 'null' and xx['label'] is not None:
                            if xx not in relations_norepeat:
                                relations_norepeat.append(xx)
                    span_names = []
                    for span in spans:
                        if span['span_name'] not in span_names:
                            span_names.append(span['span_name'])
                    relation = data['relation']
                    for re in relation:
                        if re['span_front']['span_name'] not in span_names or re['span_after']['span_name'] not in span_names:
                            relation.remove(re)
                            print(re)

                    for re in relation:
                        if 'label' in re['span_front'] and 'label' in re['span_after']:
                            if re['span_after']['label'] == '药物治疗':
                                re['span_after']['label'] = '药物'
                            if 'rel_property' not in re:
                                rel_property = ''
                            else:
                                rel_property = re['rel_property'].replace('/n', '')
                            if 'en_property' not in re['span_front']:
                                en1_prop = ''
                            else:
                                en1_prop = re['span_front']['en_property'].replace('/n', '')
                            if 'en_property' not in re['span_after']:
                                en2_prop = ''
                            else:
                                en2_prop = re['span_after']['en_property'].replace('/n', '')
                            rel = re['span_front']['label'] + '-' + re['span_after']['label']
                            sub_rel = re['rel_type']
                            en1 = re['span_front']['span_name'].replace('/n', '')
                            en2 = re['span_after']['span_name'].replace('/n', '')
                            write.writerow([rel, sub_rel, en1, en1_prop, en2, en2_prop, rel_property, p+ '/' + pa])
                        else:
                            print(re)
                    # data['spans'] = spans
                    # data['relation'] = relation
                    # export = {}
                    # resul = []
                    # resul.append(data)
                    # export['result'] = resul
                    # if os.path.exists('C:\\Users\\12504\\Desktop\\' + '儿科x' + '\\' + p + '\\'):
                    #     with open('C:\\Users\\12504\\Desktop\\' + '儿科x' + '\\' + p + '\\' + pa, 'w', encoding='utf-8') as f1:
                    #         json.dump(export, f1, ensure_ascii=False)
                    # else:
                    #     os.mkdir('C:\\Users\\12504\\Desktop\\' + '儿科x' + '\\' + p + '\\')
                    #     with open('C:\\Users\\12504\\Desktop\\' + '儿科x' + '\\' + p + '\\' + pa, 'w', encoding='utf-8') as f1:
                    #         json.dump(export, f1, ensure_ascii=False)
        # print('未去重实体数目：')
        # for label in labels:
        #     count = 0
        #     for re in relations:
        #         if re['label'] == label:
        #             count += 1
        #     print(label + ': ' + str(count))
        # print('去重实体数目：')
        # for label in labels:
        #     count = 0
        #     for re in relations_norepeat:
        #         if re['label'] == label:
        #             count += 1
        #     print(label + ': ' + str(count))
        # # print(relations_norepeat)
        # data = read_json('C:\\Users\\12504\\Desktop\\第八节支气管肺炎.json')
        # relation = data['relation']
        # for re in relation:
        #     if 'label' not in re['span_front'] or 'label' not in re['span_after'] or 'end_offset' not in re['span_front'] or 'end_offset' not in re['span_after'] or re['span_front']['end_offset'] == '' or re['span_after']['end_offset'] == '':
        #         print(re)
        # spans = data['spans']
        # for span in spans:
        #     if 'label' not in span:
        #         print(span)


