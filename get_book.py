# encoding:utf-8

import requests
import re
import time

class Sanqiushuwu(object):
    """
        这是三秋树屋类
    """
    url = 'https://www.d4j.cn'
    headers = {
        # 'Host': 'www.d4j.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.115'
    }
    def __init__(self):
        self.url = Sanqiushuwu.url

    @staticmethod
    def access_url(url=url):
        print(url)
        r = requests.get(url, headers=Sanqiushuwu.headers)
        if r.status_code == 200:
            return r
        else:
            return False
            # print('网站不可访问！现在退出。。。')
            # exit()

    @staticmethod
    def flip_over(url=url):
        c = 312
        while True:
            c += 1
            inter_url = '{}/page/{}'.format(url, c)
            if Sanqiushuwu.access_url(url):
                yield inter_url
            else:
                return False

    def get_url(self, url=url):
        r = self.access_url(url)
        content = r.text
        result = re.findall('<h2 class="kratos-entry-title-new"><a href="(.*?)">.*?</a></h2>', content)
        return result

    def get_download_url(self, url):
        r = self.access_url(url)
        content = r.text
        result = re.findall('<a class="downbtn".*?title="(.*?)" href="(.*?)".*?</a>', content)
        if result:
            title = result[0][0]
            r_1 = self.access_url(result[0][1])
            content_1 = r_1.text
            try:
                down_url = re.findall('<span class="downfile">.*?href="(.*?)".*?</span>', content_1)[0]
                down_code = re.findall('<li>百度网盘提取码 ：<font.*?>(.*?)</font></li>', content_1)[0]
                # print
            except:
                print('下载地址不存在 跳过')
                return False
            return [title, down_url, down_code]
        else:
            return False


if __name__ == '__main__':
    b = Sanqiushuwu()
    page = Sanqiushuwu.flip_over()
    while True:
        if not page:
            break
        urls = b.get_url(page.__next__())
        time.sleep(3)
        for url in urls:
            du = b.get_download_url(url)
            if du == False:
                continue
            time.sleep(3)
            with open('book.txt', 'a+', encoding='utf-8') as f:
                f.seek(0, 0)
                if not du:
                    print('没有找到下载链接')
                    continue
                elif du[0] in [re.sub(r'《|》|\n', '', x) for x in f.readlines()]:
                    print(du[0], '已存在 跳过')
                    continue
                else:
                    print(du)
                    f.seek(0, 2)
                    f.write('《'+du[0]+'》'+'\n')
                    f.write('地址：'+du[1]+' '+'密码：'+du[2]+'\n')
                    f.write('\n')

