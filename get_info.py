import random
import time
import requests
from bs4 import BeautifulSoup
from utils import get_info_data, get_md5s, init_files, save_info_data
from xmu_urls import INFO_URLS
from info import Info

md5s = []
data = []


def get_category_data():
    global data
    return [cate["category"] for cate in data]


category = get_category_data()


def get_content(url):
    time.sleep(random.random()) 
    try:
        html_data = requests.get(url, timeout=3)
        site = "/".join(url.split("/")[:3])
        html_data.encoding = html_data.apparent_encoding
        html_text = html_data.text
        soup = BeautifulSoup(html_text, 'html.parser')
        if "xmu.edu.cn" not in url:
            raise Exception
        content = soup.find('div', class_='v_news_content')
        return str(content).replace('href="/', f'href="{site}/').replace('src="/', f'src="{site}/')
    except:
        return None


def yjsy_get_list(soup, site):
    items = soup.find_all('div', class_='list-item')
    infos = []
    for item in items:
        title = item.find('a').text
        link = item.find('a')['href']
        if "http" not in link:
            link = site + "/" + link
        date = item.find('div', class_='list-item-date').text
        info = Info(title, link, date)
        # if info.md5_path in md5s:
        #     info.set_have_local_temp()
        # else:
        #     info.save_content(get_content(link))
        #     infos.append(info)
        # print(info)

        if info.md5_path not in md5s:
            info.save_content(get_content(link))
            infos.append(info)
            print(info)

    return infos


def xaxq_get_list(soup, site):
    soup = soup.find('ul', class_='news-list')
    items = soup.find_all('li')
    infos = []
    for item in items:
        title = item.find('a').text
        link = item.find('a')['href']
        if "http" not in link:
            link = site + "/" + link.replace("../", "")
        date = item.find('div', class_='news-list-date').text
        info = Info(title, link, date)
        # if info.md5_path in md5s:
        #     info.set_have_local_temp()
        # else:
        #     info.save_content(get_content(link))
        #     infos.append(info)
        # print(info)
        if info.md5_path not in md5s:
            info.save_content(get_content(link))
            infos.append(info)
            print(info)

    return infos


def xxxy_get_list(soup, site):
    soup = soup.find('div', class_='infoContent')
    items = soup.find_all('div', class_='row')[:-1]
    infos = []
    for item in items:
        title = item.find('a').text
        link = item.find('a')['href']
        if "http" not in link:
            link = site + "/" + link.replace("../../", "")
        date = item.find('div', class_='news-date').text
        info = Info(title, link, date)
        # if info.md5_path in md5s:
        #     info.set_have_local_temp()
        # else:
        #     info.save_content(get_content(link))
        #     infos.append(info)
        # print(info)
        if info.md5_path not in md5s:
            info.save_content(get_content(link))
            infos.append(info)
            print(info)
    return infos


def get_list(source_name: str, url: str):
    department, part = source_name.split("_")
    site = "/".join(url.split("/")[:3])
    html_data = requests.get(url)
    html_data.encoding = html_data.apparent_encoding
    html_text = html_data.text
    soup = BeautifulSoup(html_text, 'html.parser')
    match department:
        case "研究生院":
            infos = yjsy_get_list(soup, site)
        case "翔安校区":
            infos = xaxq_get_list(soup, site)
        case "信息学院":
            infos = xxxy_get_list(soup, site)
        case _:
            infos = []
    return infos


def update_md5s():
    global md5s
    md5s = get_md5s()


def update_datas():
    global data
    data = get_info_data()


def update_category():
    global category
    category = get_category_data()


def write_to_json(source_name: str, info: Info):
    global data
    for cate in data:
        if cate["category"] == source_name:
            cate["data"].append(info.json())
            break
    else:
        data.append({
            "category": source_name,
            "data": [info.json()]
        })

def init():
    init_files()

def update_info():
    global data
    init()
    update_md5s()
    update_datas()
    for source_name, url in INFO_URLS.items():
        infos = get_list(source_name, url)
        for info in infos:
            write_to_json(source_name, info)
        print("*"*30)
        print(f"get {len(infos)} items from {source_name}")

    for cate in data:
        cate["data"].sort(key=lambda x: x["date"], reverse=True)

    save_info_data(data)
    update_category()


def get_infos(cate: str = None):
    global data, category
    if cate is not None:
        if cate not in category:
            return []
        for cate_data in data:
            if cate_data["category"] == cate:
                return cate_data["data"]
    else:
        infos = []
        for cate_data in data:
            infos += cate_data["data"]
        infos.sort(key=lambda x: x["date"], reverse=True)
        return infos


def get_cates():
    global category
    return category


if __name__ == "__main__":
    update_info()
