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
            'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"
        }

    def login(self,uname,passowrd):
        parms = {
            'fid':'-1',
            'uname':uname,
            'password':passowrd,
            'refer':'https%253A%252F%252Fi.chaoxing.com'

        }
        resp = self.session.post(self.login_url,params=parms,headers=self.headers,verify=False)
        resp = self.session.get(self.work_url,headers=self.headers, verify=False)
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
            if len(span_all) < 4:   # 代表无剩余时间
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
    spider.login('18976992105','20040415fys')
    unfi_work = spider.parse()
    json.dump(unfi_work, open('unfi_work.json', 'w'))



