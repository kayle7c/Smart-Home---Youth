import requests
import json

def get_unfinished_homework():
    parms = {
        'username': '15529206626',
        'password': 'akdytianshi777',
    }
    headers = {
        'Content-Type': 'application/json',
    }
    result = ""
    resp = requests.post('http://127.0.0.1:5000/work',params=parms,headers=headers,verify=False)
    data = resp.json()
    for item in data['data']:
        course_name = item['course_name']  # 课程名称
        remaining_time = item['remaining_time']  # 剩余时间
        status = item['status']  # 作业状态
        work_name = item['work_name']  # 作业名称

        if status == "未提交":
            result += f"课程名称: {course_name}\n"
            result += f"剩余时间: {remaining_time}\n"
            result += f"状态: {status}\n"
            result += f"作业名称: {work_name}\n"
            result += "-" * 50 + "\n"  # 分隔线

    return result

