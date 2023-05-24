import hashlib
import json

from dao.mysql_db import Mysql
from entity.user import User
from utils.page_utils import PageUtils
from flask import Flask, request, jsonify
from utils.log import get_logger
from service.log_data import LogData

logger = get_logger()

page_query = PageUtils()
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/sum', methods=["POST"])
def sum():
    try:
        if request.method == "POST":
            req_json = request.get_json()
            a = req_json['a']
            b = req_json['b']
            return jsonify({'code': 200, 'msg': '请求成功', 'data': a + b})
    except:
        return jsonify({'code': '500', 'msg': 'error'})


@app.route('/hello_rec', methods=["POST"])
def hello_recommendation():
    try:
        if request.method == "POST":
            req_json = request.get_data()
            rec_obj = json.loads(req_json)
            user_id = rec_obj['user_id']
            return jsonify({'code': 200, 'msg': '请求成功', 'data': 'hello' + user_id})
    except:
        return jsonify({'code': '500', 'msg': 'error'})


@app.route('/hello_rec1', methods=["POST"])
def hello_recommendation1():
    try:
        if request.method == "POST":
            req_json = request.get_json()
            user_id = req_json['user_id']
            return jsonify({'code': 200, 'msg': '请求成功', 'data': 'hello' + user_id})
    except:
        return jsonify({'code': '500', 'msg': 'error'})


@app.route('/rec/get_rec_list', methods=["POST"])
def get_rec_list():
    if request.method == "POST":
        req_json = request.get_json()
        page_num = req_json['page_num']
        page_size = req_json['page_size']
        try:
            data = page_query.get_data_with_page(page_num, page_size)
            return jsonify({'code': 200, 'msg': '请求成功', 'data': data})
        except Exception as e:
            logger.error(f'服务器异常:{e}')
            return jsonify({'code': '500', 'msg': 'error'})
    return jsonify({'code': 500, 'msg': 'error'})


@app.route("/rec/register", methods=["POST"])
def register():
    if request.method == "POST":
        req_json = request.get_json()
        user = User()
        user.user_name = req_json['username']
        user.nick = req_json['nick']
        user.age = req_json['age']
        user.gender = req_json['gender']
        user.city = req_json['city']
        user.pwd = str(hashlib.md5(req_json['password'].encode()).hexdigest())

        try:
            mysql = Mysql()
            sess = mysql._DBSession()
            if sess.query(User.id).filter(User.user_name == user.user_name).count() > 0:
                return jsonify({"code": 500, "msg": "用户已存在！"})
            sess.add(user)
            sess.commit()
            sess.close()
            return jsonify({'code': 200, "msg": "注册成功！"})
        except Exception as e:
            logger.error(f'服务器异常:{e}')
            return jsonify({'code': 500, "msg": "error"})
    return jsonify({'code': 500, 'msg': 'error'})


@app.route("/rec/login", methods=["POST"])
def login():
    if request.method == "POST":
        req_json = request.get_json()
        user_name = req_json['username']
        pwd = str(hashlib.md5(req_json['password'].encode()).hexdigest())
        try:
            mysql = Mysql()
            sess = mysql._DBSession()
            res = sess.query(User.id).filter(User.user_name == user_name, User.pwd == pwd)
            if res.count() > 0:
                for x in res.all():
                    data = {'userid': str(x[0])}
                    info = jsonify({'code': 200, "msg": "登录成功！", 'data': data})
                    return info
            else:
                return jsonify({'code': 500, "msg": "用户名密码错误！"})

        except Exception as e:
            logger.error(f'服务器异常：{e}')
            return jsonify({'code': 500, 'msg': 'error'})
    return jsonify({'code': 500, 'msg': 'error'})


@app.route("/rec/ops", methods=["POST"])
def ops():
    if request.method == "POST":
        req_json = request.get_json()
        user_id = req_json['user_id']
        content_id = req_json['content_id']
        title = req_json['title']
        type = req_json['ops']
        # 仅支持收藏，点击，点赞操作
        if type not in ['collections','likes','read']:
            return jsonify({'code': 500, "msg": "操作失败！"})
        log_data = LogData()
        try:
            mysql = Mysql()
            sess = mysql._DBSession()
            res = sess.query(User.id).filter(User.id == user_id)
            if res.count() > 0:
                key = "news_detail:" + content_id
                if log_data.insert_log(user_id, content_id, title, type) and log_data.modify_article_detail(key, type):
                    return jsonify({'code': 200, "msg": "操作成功！"})
                else:
                    return jsonify({'code': 500, "msg": "操作失败！"})
            else:
                return jsonify({'code': 500, "msg": "用户名不存在！"})
        except Exception as e:
            logger.error(f'服务器异常：{e}')
            return jsonify({'code': 500, 'msg': 'error'})
    return jsonify({'code': 500, 'msg': 'error'})


if __name__ == '__main__':
    app.run()
