import datetime
from flask import Flask, session, jsonify, request
from snownlp import SnowNLP

from database.config import db, SQLALCHEMY_DATABASE_URI
from model.User import User
from analysis import calculate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = 'weibo_topic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/recently', methods=['POST'])
def recently_topic():
    """
    偏好分析
    1.商家路线热度排序分析
    2.商家路线热度汇总分析
    :return:
    """
    data1 = calculate.hot_buying()
    data2 = calculate.get_merchant_ranking_stats()
    result = {'amount': data2, 'code': 20000, 'buyings': data1}
    return jsonify(result)


@app.route('/wordCloud', methods=['POST'])
def weekly_wc():
    """
    商家路线图谱
    :return:
    """
    data = calculate.buying_word_cloud()
    result = {'code': 20000, 'data': data}
    return jsonify(result)





@app.route('/region', methods=['POST'])
def region():
    """
    客源分析
    :return:
    """
    data = calculate.region()
    return jsonify({'code': 20000, 'data': data})


@app.route('/price', methods=['GET'])
def getPrice():
    """
    游客团购偏好分析
    :return:
    """
    data = calculate.getPrice()
    result = {'code': 20000, 'data': data}
    return jsonify(result)


@app.route('/att', methods=['POST'])
def getAtt():
    """
    景区分析
    :return:
    """
    param = request.get_json()
    data = calculate.getAtt(param)
    result = {'code': 20000, 'data': data}
    return jsonify(result)
@app.route('/attGetAll', methods=['GET'])
def attGetAll():
    """
    景区分析
    :return:
    """
    data = calculate.attGetAll()
    result = {'code': 20000, 'data': data}
    return jsonify(result)


@app.route('/logout', methods=['POST'])
def logout():
    """
    注销
    """
    session.clear()
    data = {'data': '', 'code': 20000}
    return jsonify(data)


@app.route('/info', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 获取请求的数据
    data = request.get_json()
    # 如果是GET请求并且已经登录过了
    if (request.method == 'GET') and (session.get('userid') is not None):
        # 获取用户信息
        user = User().userinfo(userid=session['userid'])
        # 将用户信息序列化后返回
        data = {'data': user.serialize(), 'code': 20000}
        return jsonify(data)
    # 如果是POST请求
    if request.method == 'POST':
        # 验证登录信息
        user = User()
        user = user.valid_login(username=data['username'], password=data['password'])
        # 如果登录成功
        if user:
            # 将用户信息保存到session中
            session['user'] = str(user.username)
            session['userid'] = str(user.id)
            # 将用户信息序列化后返回
            data = {'data': user.serialize(), 'code': 20000}
            return jsonify(data)
        # 如果登录失败，返回错误信息
        else:
            data['error'] = '错误的用户名或密码!'
    # 如果既不是GET请求也不是POST请求，或者已经登录失败，则返回data变量
    return data



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/allComments', methods=['POST'])
def allComments():
    """
    获取所有评论的情感值
    :return:
    """
    data = calculate.getAllComments()
    if not not data:
      result = {'code': 20000, 'data': data}
    else:
      result = {'code': 20001, 'data': data}
    return jsonify(result)


if __name__ == '__main__':
    app.run()
