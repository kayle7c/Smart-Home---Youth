import requests
from bs4 import BeautifulSoup
import json


class ChaoxingSpider(object):
    def __init__(self):
        self.data_list = []
        self.html = None
        self.session = requests.Session()
        self.login_url = 'https://passport2.chaoxing.com/fanyalogin'
        self.work_url = 'https://mooc1-api.chaoxing.com/mooc-ans/work/stu-work'
        self.result = []

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://passport2.chaoxing.com/',
            # 'Sec-CH-UA': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            # 'Sec-CH-UA-Mobile': '?0',
            # 'Sec-CH-UA-Platform': '"Windows"',
            # 'Sec-Fetch-Dest': 'document',
            # 'Sec-Fetch-Mode': 'navigate',
            # 'Sec-Fetch-Site': 'same-site',
            # 'Sec-Fetch-User': '?1',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }

    def login(self, uname, passowrd):
        parms = {
            'fid': '-1',
            'uname': uname,
            'password': passowrd,
            'refer': 'https://passport2.chaoxing.com/'

        }

        # 隧道域名:端口号
        tunnel = "a349.kdltps.com:15818"

        # 用户名密码方式
        username = "t14365858092948"
        password = "2qb9fyye"
        proxies = {
            "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
            "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
        }

        resp = self.session.post(self.login_url, params=parms, headers=self.headers, verify=False,
                                 allow_redirects=False,proxies=proxies)
        if resp.status_code != 200:
            raise Exception(f"Login failed with status code: {resp.status_code} {resp.headers.get('Location')}")

        resp = self.session.get(self.work_url, headers=self.headers, verify=False)
        if resp.status_code != 200:
            raise Exception(f"Failed to fetch work list with status code: {resp.status_code}")

        self.html = resp.text
        # print(self.html)

    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        option_divs = soup.find_all('div', {'role': 'option'})
        for div in option_divs:
            # 提取测验名称
            quiz_name = div.find('p')
            if quiz_name is None:
                continue
            # 提取作业状态
            status = div.find('span', class_='status')
            if status is None:
                continue
            # 获取所有的 span
            span_all = div.find_all('span')
            if len(span_all) < 4:  # 代表无剩余时间
                continue

            # 提取课程名称
            course_name = div.find_all('span')[1].text.strip()

            # 提取剩余时间
            remaining_time = div.find('span', class_='fr').text.strip()

            # 整理成字典
            data = {
                "work_name": quiz_name.text,
                "status": status.text,
                "course_name": course_name,
                "remaining_time": remaining_time
            }

            self.data_list.append(data)
        return self.data_list


if __name__ == '__main__':
    spider = ChaoxingSpider()
    spider.login('18976992105', '20040415fys')
    unfi_work = spider.parse()
    print(unfi_work)
    json.dump(unfi_work, open('unfi_work.json', 'w'))