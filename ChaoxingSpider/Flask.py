from flask import Flask, request, jsonify
from chaoxingSpider import ChaoxingSpider  # 假设 ChaoxingSpider 在 your_spider_module 模块中
import json

app = Flask(__name__)


@app.route('/work', methods=['GET', 'POST'])
def login_and_parse():
    try:
        # 获取 POST 请求的 JSON 数据
        username = request.args.get('username')
        password = request.args.get('password')
        # 检查是否包含账号和密码
        if not username or not password:
            return jsonify({"status": "error", "message": "缺少账号或密码"}), 400


        # 创建爬虫实例并登录
        spider = ChaoxingSpider()
        spider.login(username, password)

        # 获取 unfi_work 数据
        unfi_work = spider.parse()

        # 返回 JSON 数据
        return jsonify({
            "status": "success",
            "data": unfi_work
        }), 200

    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)