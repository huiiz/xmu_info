import hashlib
import json
import os


def calc_md5(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()


def get_md5s():
    ls = []
    # 获取data目录下所有文件的文件名
    for file in os.listdir('data'):
        # 如果文件名以.html结尾
        if file.endswith('.html'):
            # 将文件名去掉.html后缀，加入ls
            ls.append(file[:-5])
    return ls


def get_temp_content(md5_path):
    # TODO: 数据该从内存读取，无内容则从GitHub远程获得
    try:
        with open(f"data/{md5_path}.html", 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "未找到缓存文件"


def get_info_data():
    with open('data/info.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def save_info_data(data):
    with open('data/info.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def init_files():
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/info.json'):
        with open('data/info.json', 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4, ensure_ascii=False)