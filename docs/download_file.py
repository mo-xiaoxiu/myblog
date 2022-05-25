import urllib.request
import requests
import re, os
from urllib.parse import quote
import ssl


ssl._create_default_https_context = ssl._create_unverified_context

def get_file(url):
    '''
    递归下载网站的文件
    :param url:
    :return:
    '''

    if isFile(url):
        try:
            download(url)
        except Exception as e:
            print(url)
            print("download failed : " + str(e))
            pass
    else:
        urls = get_url(url)
        for u in urls:
            get_file(u)

def isFile(url):
    '''
    判断一个链接是否是文件
    :param url:
    :return:
    '''
    if url.endswith('/'):
        return False
    else:
        return True

def download(url):
    '''
    :param url:文件链接
    :return: 下载文件，自动创建目录
    '''
    full_name = url.split('//')[-1]
    url = quote(url, safe='/:?=@')
    filename = full_name.split('/')[-1]
    dirname = "/".join(full_name.split('/')[:-1])
    if os.path.exists(dirname):
        pass
    else:
        os.makedirs(dirname, exist_ok=True)
    print(url)
    urllib.request.urlretrieve(url, full_name)

def get_url(base_url):
    '''
    :param base_url:给定一个网址
    :return: 获取给定网址中的所有链接
    '''
    text = ''
    try:
        text = requests.get(quote(base_url, safe='/:?=@')).text
    except Exception as e:
        print("error - > ",base_url,e)
        pass
    reg = '<a href="(.*)">.*</a>'
    urls = [base_url + url for url in re.findall(reg, text) if url != '../']
    return urls

if __name__ == '__main__':
    '''
    遍历list.txt文件中的 URL，并下载
    '''
    with open('list.txt', 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        url_list = []
        for line in lines:
            get_file(line.strip('\n'))
