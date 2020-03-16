import urllib.request
import re
import time
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip',
    'Connection': 'close',
    'Referer': None
    }

# originalUrl = "https://www.meitulu.com/item/20538.html"
originalUrl = (True, "www.baidu.com")
downloadLocation = "E:/xxx"
url = 'xxx'
mainUrl = "xxx"


def getUrl(url):
    interUrl = "{}/{}.html".format("/".join(url.split("/")[:-1]),
                                   str(int(url.split("/")[-1]
                                           .split(".")[0]) - 1))
    try:
        urllib.request.urlopen(interUrl)
    except Exception as e:
        print(interUrl, str(e))
        return False, interUrl
    else:
        print(interUrl, "正在检索...")
        return True, interUrl


def getSeriesUrl(url):
    fileName = downloadLocation + '/' + r'url.txt'
    if os.path.exists(fileName):
        with open(fileName, 'r') as f:
            return f.readlines()
    c = 2
    urlList = []
    interUrl = url
    response = urllib.request.urlopen(url)
    content = response.read().decode("utf-8")
    title = re.findall("<title>(.*?)</title>", content)[0]
    print(title, '正在获取URL...')
    while True:
        time.sleep(1)
        try:
            print("正在获取URL", "[", c - 1, "]")
            response = urllib.request.urlopen(interUrl)
            content = response.read().decode("utf-8")
        except Exception as e:
            print(title, 'URL获取完毕...')
            break
        else:
            findout = re.findall('<a href="(.*?)" target="_blank">', content)
            urlList.extend(findout)
            interUrl = url + str(c) + ".html"
            c += 1
    print(urlList)
    with open(fileName, 'w') as f:
        for url in urlList:
            f.write(url)
    return urlList


def getPic(url):
    picUrl = []
    count = 2
    interUrl = url
    response = urllib.request.urlopen(interUrl)
    content = response.read().decode("utf-8")
    title = re.findall("<title>(.*?)</title>", content)[0]
    dirname = downloadLocation + "/" + title
    if os.path.exists(dirname):
        print(dirname, "已存在, 无需下载。")
        return False

    while True:
        try:
            response = urllib.request.urlopen(interUrl)
            content = response.read().decode("utf-8")
            findout = re.findall('<img src="(.*?)" .*?">', content)
            # print(findout)
            interUrl = "{}/{}_{}.html".format(
                "/".join(url.split("/")[:-1]),
                url.split("/")[-1].split(".")[0], str(count))
            # print(interUrl)
        except Exception:
            print(title, "解析完毕！")
            break
        else:
            picUrl.extend(findout)
            count += 1
    return title, picUrl


# print(getPic(url))


def downloadPic(title, urls):
    dirname = downloadLocation + "/" + title
    os.mkdir(dirname)
    for url in urls:
        fileName = url.split("/")[-1]
        time.sleep(0.3)
        try:
            print(title, url, "正在下载...")
            with open(dirname + "/" + fileName, "wb") as f:
                f.write(urllib.request.urlopen(url).read())
        except Exception:
            print(title, url, "下载失败！")


if __name__ == "__main__":
    a = getSeriesUrl(url)
    print(a)
    for i in a:
        interUrl = i
        picUrls = getPic(interUrl)
        if picUrls:
            title = picUrls[0]
            urls = picUrls[1]
            downloadPic(title, urls)
    # c = 0
    # while True:
    #     if originalUrl[0]:
    #         picUrls = getPic(originalUrl[1])
    #         if picUrls:
    #             title = picUrls[0]
    #             urls = picUrls[1]
    #             downloadPic(title, urls)
    #         originalUrl = getUrl(originalUrl[1])
    #     elif not originalUrl[0] and c < 1000:
    #         originalUrl = getUrl(originalUrl[1])
    #         c += 1
    #     else:
    #         break

