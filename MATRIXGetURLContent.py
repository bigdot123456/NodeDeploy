import bs4
import chardet
import csv
import hashlib
import logging
import os
import platform
import psutil
import re
import requests
import shutil
import signal
import socket
import stat
import subprocess
import sys
import time
import urllib
import urllib.request
import zipfile
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from tqdm import tqdm
from urllib import request
from urllib.parse import urljoin
from urllib.request import urlopen
from urllib.request import urlretrieve


def download_from_url(url, dst):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    file_size = int(urlopen(url).info().get('Content-Length', -1))

    """
    print(urlopen(url).info())
    # output
    Server: AliyunOSS
    Date: Tue, 19 Dec 2017 06:55:41 GMT
    Content-Type: application/octet-stream
    Content-Length: 29771146
    Connection: close
    x-oss-request-id: 5A38B7EDCE2B804FFB1FD51C
    Accept-Ranges: bytes
    ETag: "9AA9C1783224A1536D3F1E222C9C791B-6"
    Last-Modified: Wed, 15 Nov 2017 10:38:33 GMT
    x-oss-object-type: Multipart
    x-oss-hash-crc64ecma: 14897370096125855628
    x-oss-storage-class: Standard
    x-oss-server-time: 4
    """
    filename = dst
    # filename = "/home/mydir/test.txt"

    # 将文件路径分割出来

    file_dir = os.path.split(filename)[0]

    # 判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
    if not os.path.isdir(file_dir):
        print(f"Download Program Will create directory {file_dir}")
        os.makedirs(file_dir)

    # 然后再判断文件是否存在，如果不存在，则创建
    if not os.path.exists(filename):
        # os.system(r'touch %s' % filename)
        print(f"opening {filename}....")
        with open(filename, "a") as f:
            pass

    # 断点续传
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size

    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


def findAllLink(url):
    '''
    提取网页中的超链接
    '''

    # url = "http://blog.csdn.net"
    # 2.根据需求构建好链接提取的正则表达式
    pattern1 = '<.*?(href=".*?").*?'
    # 3.模拟成浏览器并爬取对应的网页 谷歌浏览器
    headers = {'User-Agent',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    data = opener.open(url).read().decode('utf8')
    # 4.根据2中规则提取出该网页中包含的链接
    content_href = re.findall(pattern1, data, re.I)
    # print(content_href)
    # 5.过滤掉重复的链接
    #    # 列表转集合(去重) list1 = [6, 7, 7, 8, 8, 9] set(list1) {6, 7, 8, 9}
    set1 = set(content_href)
    # print(set1)

    # 6.后续操作，比如打印出来或者保存到文件中。
    file_new = "./href.txt"
    with open(file_new, 'w') as f:
        for i in set1:
            f.write(i)
            f.write("\n")
    f.close()

    print(f"已经生成文件{file_new}")

    return set1


def findAllLink1(url):
    headers = ("User-Agent",
               "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
    file = urllib.request.urlopen(url).read()
    file = file.decode('utf-8')
    pattern = '(https?://[^\s)";]+(\.(\w|/)*))'
    links = re.compile(pattern).findall(file)
    # 去重
    links = list(set(links))

    # print(links)
    return links


def findAllLink2(url):
    file = open('result.csv', 'w', encoding='utf-8', newline='')
    cw = csv.writer(file)
    cw.writerow(['URL', 'Anchor'])

    resp = requests.get(url)
    encoding = chardet.detect(resp.content)["encoding"]
    # print(encoding)
    resp.encoding = encoding
    links = re.findall(r'<a.*?href="(.*?)".*?>(.*?)</a>', resp.text, re.S | re.I)
    for link in links:
        a = urljoin(url, link[0]), link[1]
        print(a)
        cw.writerow(a)

    file.close()

    links = list(set(links))  # 标准去重

    return links


def findAllLink3(url):
    # 获取请求
    req = urllib.request.Request(url)
    # 打开页面
    webpage = urllib.request.urlopen(req)
    # 读取页面内容
    html = webpage.read()
    # 解析成文档对象
    soup = bs4.BeautifulSoup(html, 'html.parser')  # 文档对象
    # 非法URL 1
    invalidLink1 = '#'
    # 非法URL 2
    invalidLink2 = 'javascript:void(0)'
    # 集合
    links = set()
    # 计数器
    mycount = 0
    # 查找文档中所有a标签
    for k in soup.find_all('a'):
        # print(k)
        # 查找href标签
        link = k.get('href')
        # 过滤没找到的
        if (link is not None):
            # 过滤非法链接
            if link == invalidLink1:
                pass
            elif link == invalidLink2:
                pass
            elif link.find("javascript:") != -1:
                pass
            else:
                mycount = mycount + 1
                # print(mycount,link)
                links.add(link)
    # print("打印超链接个数:",mycount)
    # print("打印超链接列表",result)

    f = open(r'result.txt', 'w', encoding='utf-8')  # 文件路径、操作模式、编码  # r''
    for a in links:
        f.write(a + "\n")
    f.close()
    print("\r\n扫描结果已写入到result.txt文件中\r\n")

    links = list(set(links))  # 标准去重
    return links


def findAllLink4(url):
    # 获取请求
    html = urlopen(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')  # 文档对象
    links = []
    t1 = soup.find_all('a')
    for t2 in t1:
        t3 = t2.get('href')
        links.append(t3)

    links = list(set(links))  # 标准去重
    return links


def findAllLink5(url):
    r = requests.get(url)
    status_code = r.status_code
    content = bs4.BeautifulSoup(r.content.decode("utf-8"), "lxml")

    element = content.find_all('a')
    # element[26].get('href')

    atag = content.find_all('a')
    hrefs = [item.get('href') for item in atag if item.get('href')]

    t = content.find('a', atrrs={'download': 'gman'})

    links = hrefs
    links = list(set(links))  # 标准去重

    return links


def findAllLink6(url, verbose=False):
    r = requests.get(url)
    status_code = r.status_code
    content = bs4.BeautifulSoup(r.content.decode("utf-8"), "lxml")
    links = set()
    for link in content.findAll('a'):
        if link.has_attr('href'):
            href = str(link.get('href'))
            if href.startswith('http'):
                links.add(href)
                if verbose:
                    print(link.get('href'))

    links = list(set(links))  # 标准去重

    return links


def findAllLink7(url):
    page = requests.get(url)
    a = BeautifulSoup(page.text, "lxml").findAll('a')
    links = dict(map(lambda i: {i.text.strip(), i.attrs['href']}, a))

    for item in links:
        if ".zip" in links[item] and "www.matrix.io" in links[item]:
            pzip_r = requests.get(links[item])
            with open(item + ".zip", "wb") as zip_file:
                zip_file.write(pzip_r.content)

    links = list(set(links))  # 标准去重

    return links


def findAllLink8(url):
    r = requests.get(url)
    r.encoding = 'gb2312'

    # print("\n Happy open.....1!")
    # 利用 re （太黄太暴力！）
    links1 = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", r.text)
    # for link in links1:
    #     print(link)

    # print("\n Happy open.....2!")
    # 利用 BeautifulSoup4 （DOM树）
    links2 = set()
    soup = BeautifulSoup(r.text, 'lxml')
    for a in soup.find_all('a'):
        link = a['href']
        links2.add(link)
        # print(link)

    # print("\n Happy open.....3!")

    # 利用 lxml.etree （XPath）
    links3 = set()
    tree = etree.HTML(r.text)
    for link in tree.xpath("//@href"):
        links3.add(link)
        # print(link)

    # print("\n Happy open.....4!")

    links4 = set()
    soup = BeautifulSoup(r.text, 'lxml')
    for iframe in soup.find_all('iframe'):
        url_ifr = iframe['src']  # 取得当前iframe的src属性值

        rr = requests.get(url_ifr)
        rr.encoding = 'gb2312'

        soup_ifr = BeautifulSoup(rr.text, 'lxml')

        for a in soup_ifr.find_all('a'):
            link = a['href']
            m = re.match(r'http:\/\/.*?(?=\/)', link)
            # print(link)
            if m:
                links4.add(m.group(0))

    # 利用selenium（要开浏览器！）
    # driver = webdriver.Chrome()
    # driver.get(url)
    # for link in driver.find_elements_by_tag_name("a"):
    #     print(link.get_attribute("href"))
    # driver.close()
    # print("\n Finish Display....!")

    links = links1
    links = list(set(links))  # 标准去重
    return links


def get_static_url_content(url, encoding='utf-8', timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    '''
    获取静态网页内容
    :param url:         网页url
    :param encoding:    网页编码
    :param timeout:     设置超时
    :return:
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url, headers=headers)
    html = urlopen(req, timeout=timeout)
    bsObj = BeautifulSoup(html.read(), "html.parser", from_encoding=encoding)
    return bsObj


def get_driver_url_content(url, encoding='utf-8', timeout=3):
    '''
    使用浏览器获取动态内容
    :param url:         网页url
    :param encoding:    网页编码
    :param timeout:     设置超时
    :return:
    '''
    chromedriver_path = '/path/to/chromedriver'
    driver = webdriver.Chrome(executable_path=chromedriver_path)
    # 也可以使用phantomJS
    # driver =webdriver.Phantomjs(executable_path="/path/to/phantomjs")
    driver.get(url)
    time.sleep(timeout)
    bsObj = BeautifulSoup(driver.page_source, 'html.parser', from_encoding=encoding)
    driver.close()
    return bsObj


def load_appendix(url, filename):
    '''
    下载附件, 将URL下载到filname里面
    :param url:         附件 url(附件文档和图片均可)
    :param filename:    保存的文件名
    :return:
    '''
    urlretrieve(url, filename)


def filterlink(links, filename):
    filterlinks = set()
    for item in links:
        for singlefile in filename:
            if singlefile in links[item]:
                filterlinks.add(item)

    filterlinks = list(set(filterlinks))  # 标准去重

    return filterlinks


def filterlink1(links, filename):
    return filter(lambda x: filename in x, links)


def unzipfile(zipfilename, dir):
    zip_ref = zipfile.ZipFile(zipfilename, 'r')
    if os.path.exists(dir):
        print(f"Delete the outdated download directory {dir}")
        shutil.rmtree(dir)

    zip_ref.extractall(dir)
    zip_ref.close()


def cpfile(filename, dir):
    # if os.path.exists(dir):
    try:
        shutil.copy(filename, dir)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())


def finddir(startdir, target):
    try:
        os.chdir(startdir)  # 切换目录
    except:
        return
    for new_dir in os.listdir(os.curdir):  # 列表出该目录下的所有文件(返回当前目录'.')
        print(new_dir)
        if new_dir == target:
            filefullname = os.getcwd() + os.sep + new_dir
            print(f"find file with filefullname")
            return filefullname
        if os.path.isdir(new_dir):  # 判断路径是否存在
            finddir(new_dir, target)
            os.chdir(os.pardir)  # 切换到当前目录的父目录


def searchFile(key, startPath='.'):
    if not os.path.isdir(startPath):
        raise ValueError
    l = [os.path.join(startPath, x) for x in os.listdir(startPath)]  # 列出所有文件的绝对路径
    # listdir出来的相对路径 不能用于 isfile  abspath只能用在当前目录
    filelist = [x for x in l if os.path.isfile(x) if key in os.path.splitext(os.path.basename(x))[0]]  # 文件
    # 只查找文件名中  不包括后缀 文件路径
    if not hasattr(searchFile, 'basePath'):  # 把函数当成类 添加属性
        searchFile.basePath = startPath  # 只有第一次调用才会赋值给basePath
    outmap = map(lambda x: os.path.relpath(x, searchFile.basePath), filelist)  # 转换成相对于初始路径的相对路径

    outlist = list(outmap)

    dirlist = [x for x in l if os.path.isdir(x)]  # 目录
    for dir in dirlist:
        outlist = outlist + searchFile(key, dir)

    return outlist


# def cpfile(filename,dir):
def out_md5(src):
    # 简单封装
    m = hashlib.md5()
    m.update(src.encode('utf-8'))
    return m.hexdigest()


def check_md5(filename):
    try:
        with open('1.txt', 'r') as f:
            src = f.read()
            m1 = out_md5(src)
            # print(m1)
        return m1
    except IOError as e:
        logging.error(e)
        return 0


def check_hash(filename, method='md5'):
    try:
        if (method.lower() == 'md5'):
            result = hashlib.md5(open(filename, 'rb').read()).hexdigest()
        elif (method.lower() == 'sha-1'):
            result = hashlib.sha1(open(filename, 'rb').read()).hexdigest()
        elif (method.lower() == 'sha-256'):
            result = hashlib.sha256(open(filename, 'rb').read()).hexdigest()
        elif (method.lower() == 'sha-512'):
            result = hashlib.sha512(open(filename, 'rb').read()).hexdigest()
        else:
            print('[-]Please input a correct encryption algorithm.')

        print(result)
        return result
    except:
        print('[*]Usage: python check_hash.py [Filename] [MD5|SHA-1|SHA-256|SHA-512]')
        print('[-]Please input a correct filename.')


import datetime


# 获取时间函数，把当前时间格式化为str类型nowdate.strftime('%Y-%m-%d %H:%M:%S')
def getLastDate():
    print("当前时间： ", time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())))
    return datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')


def searchAllFile(dir_path):
    try:
        for root, dirs, files in os.walk(dir_path):
            for filename in files:
                print("file:%s\n" % filename)
            for dirname in dirs:
                print("dir:%s\n" % dirname)
    except IOError as e:
        print("error with IO1!")
        logging.error(e)
        return ''


def searchFilename(name, dir_path='.'):
    try:
        for root, dirs, files in os.walk(dir_path):  # path 为根目录
            # if name in dirs or name in files:
            if name in files:
                # flag = 1      #判断是否找到文件
                # dirs = str(dirs)
                root = str(root)
                return os.path.join(root, name)
        return ''
    except IOError as e:
        print("error with IO!")
        logging.error(e)
        return 0


def searchDirname(name, dir_path='.'):
    try:
        for root, dirs, files in os.walk(dir_path):  # path 为根目录
            # if name in dirs or name in files:
            if name in dirs:
                # flag = 1      #判断是否找到文件
                # dirs = str(dirs)
                root = str(root)
                return os.path.join(root, name)
        return ''

    except IOError as e:
        print("error with IO2!")
        logging.error(e)
        return 0


def autoDownloadGman(infourl='https://www.matrix.io/downloads/', backupdir="backup",
                     downloadbaseURL="https://www.matrix.io"):
    links = findAllLink8(infourl)

    # load_appendix(url,"a.txt")
    result = filterlink1(links, "zip")

    # downloadbaseURL = "https://www.matrix.io"

    timestamp = getLastDate()
    #timestamp = "2019-06-14_16_58_17"

    # backupdir = "backup"
    workdir = "work"

    sysstr = platform.system()
    if (sysstr == "Windows"):
        # print("Now We will do Windows tasks")
        Platform = "Windows"
        GmanDir = "gman(windows)"
        GmanName = "gman.exe"
    elif (sysstr == "Linux"):
        # print("Now We will do Linux tasks")
        Platform = "Linux"
        GmanDir = "gman(linux)"
        GmanName = "gman"
    elif (sysstr == "Darwin"):
        # print("Now We will do MacOS tasks")
        Platform = "Darwin"
        GmanDir = "gman(mac)"
        GmanName = "gman"
    else:
        Platform = "Windows"
        GmanDir = "gman(windows)"
        GmanName = "gman.exe"
        # print("Other System tasks")

    for i in result:
        httpURLname = f"{downloadbaseURL}{i}"
        destfilename = os.path.basename(i)

        destfullfilename = f"./Download/{timestamp}/{destfilename}"

        download_from_url(httpURLname, destfullfilename)

        # (filepath, tempfilename) = os.path.split(filename)
        # (shotname, extension) = os.path.splitext(tempfilename)
        (shotname, extension) = os.path.splitext(destfilename)

        print(f"unzip {destfullfilename} in {backupdir}/{shotname}")
        unzipfile(destfullfilename, f"{backupdir}/{shotname}")

    Mypath = searchDirname(GmanDir, backupdir)
    if Mypath == "":
        print("error in unzip files")
        return ""

    Myfile = searchFilename(GmanName, Mypath)
    if Myfile == "":
        print(f"Can't open the main execute file {GmanName}")
        return ""

    return Myfile


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(f"{path}创建成功")
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        isdir = os.path.isdir(path)
        if isdir:
            print(f"{path}目录已存在")
            return False
        else:
            print(f"{path}文件已存在，需要删除")
            os.remove(path)
            os.makedirs(path)
            print(f"{path}创建成功")
            return True


def autoDeployGman(fileName, workdir='work'):
    if not os.path.exists(fileName):
        print("please Check file, It doesn't exist!")
        return -1

    chaindir = workdir + os.sep + 'chaindata'
    mkdir(workdir)
    mkdir(chaindir)

    (filepath, tempfilename) = os.path.split(fileName)
    fileGmandest = workdir + os.sep + tempfilename
    print(f"Copy {fileName} to {workdir} & chmod 777 {fileGmandest}")
    cpfile(fileName, workdir)
    os.chmod(fileGmandest, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # mode:777

    fileGenesis = 'MANGenesis.json'
    fileman = 'man.json'

    fileGenesisSrc = filepath + os.sep + fileGenesis
    fileGenesisdest = workdir + os.sep + fileGenesis

    filemanSrc = filepath + os.sep + 'chaindata' + os.sep + fileman
    filemandest = workdir + os.sep + 'chaindata' + os.sep + fileman

    if os.path.exists(fileGenesisdest):
        print(f"We don't change {fileGenesisdest}, If you want change it, please first delete it in {workdir}")
    else:
        print(f"Copy {fileGenesisSrc} to {workdir}")
        cpfile(fileGenesisSrc, workdir)

    if os.path.exists(filemandest):
        print(f"We don't change {filemandest}, If you want change it, please first delete it in {workdir}")
    else:
        print(f"Copy {filemanSrc} to {workdir}")
        cpfile(filemanSrc, chaindir)


def autoRmOldGman(fileName, workdir='work'):
    (filepath, tempfilename) = os.path.split(fileName)
    fileGmandest = workdir + os.sep + tempfilename
    if os.path.exists(fileGmandest):
        # 删除文件，可使用以下两种方法。
        os.remove(fileGmandest)
        # os.unlink(my_file)
    else:
        print("Old Gman doesn't exists!")


def killpid(pid):
    try:
        a = os.kill(pid, signal.SIGKILL)
        print('已杀死pid为%s的进程,　返回值是:%s' % (pid, a))
    except OSError:
        print('没有如此进程!!!')


def processinfo(processName):
    pids = psutil.pids()
    pidlist = []
    for pid in pids:
        # print(pid)
        p = psutil.Process(pid)
        # print(p.name)
        if processName in p.name():
            print(pid)
            pidlist.append(pid)  # 如果找到该进程则打印它的PID，返回true

    return pidlist  # 没有找到该进程，返回false


def autokillGman():
    pidlist = processinfo('gman')

    for pid in pidlist:
        killpid(pid)

# cd work
# ./gman --datadir ./chaindata  init MANGenesis.json

def initGman(workdir='work'):
    rootdir = os.getcwd()
    os.chdir(workdir)
    cmd = f".{os.sep}gman --datadir ./chaindata  init MANGenesis.json"
    print(f"Init Gman with command:\ncd {workdir};\n.{os.sep}gman --datadir ./chaindata  init MANGenesis.json \n\n")
    child1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    outs, errs = child1.communicate()

    # output=str(outs).decode('string_escape')
    output = str(outs, 'utf-8')
    print(f"cmd execute result:\n{output}")
    os.chdir(rootdir)


if __name__ == '__main__':
    url = 'https://www.matrix.io/downloads/'
    Myfile = autoDownloadGman(url)
    autoDeployGman(Myfile)
    #autoRunGman()
    # autokillGman()
    # autoRmOldGman('gman')
    initGman()
    #autoRunNormalGman()
