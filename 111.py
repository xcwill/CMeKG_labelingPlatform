import json, os, csv


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f1:
        export = json.load(f1)
    result = export['result']
    data = result[0]
    return data
res = []
def parse_data(data):
    relation = data['relation']
    for re in relation:
        if re['rel_property'] != '':
            res.append(re)


def write_json(data):
    with open('C:\\Users\\12504\\Desktop\\x.json', 'w',encoding='utf-8') as f1:
        json.dump(data, f1, ensure_ascii=False)
    with open('C:\\Users\\12504\\Desktop\\x.csv', 'w', newline='', encoding='utf-8')as f:
        write = csv.writer(f, dialect='excel')
        for re in data:
            line = [re['rel_type'], re['span_front']['span_name'], re['span_after']['span_name'], re['rel_property']]
            write.writerow(line)


def main():
    # path = 'E:\\医疗知识图谱\\best_practice_txt_new\\3_aetiology.txt'
    filelist = os.listdir('C:\\Users\\12504\\Desktop\\106种疾病\\')
    for file in filelist:
        files = os.listdir('C:\\Users\\12504\\Desktop\\106种疾病\\' + file + '\\')
        for fi in files:
            path = 'C:\\Users\\12504\\Desktop\\106种疾病\\'+file + '\\' + fi
            data = read_json(path)
            parse_data(data)
    print(len(res))
    write_json(res)


if __name__ == '__main__':
    main()
