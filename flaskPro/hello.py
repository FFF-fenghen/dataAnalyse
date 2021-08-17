import datetime

from flask import Flask, render_template, request

app = Flask(__name__)  # 初始化一个对象叫app，将自身的框架导入到程序中


# 路由解析，通过用户访问的路径，匹配相应的函数，返回的函数就是自己下面定义的函数
# @app.route('/index/<name>')
# def hello_world(name):
#     return '你好,%s' % name

#  通过访问路径，获取数字类型
# @app.route('/index/<int:id>')
# def hello_world(id):
#     return '你好,%d 的会员' % id

# @app.route('/')
# def hello_world():
#     time = datetime.date.today()
#     name = ['a','b','c']
#     task = {'任务':'打扫卫生', '时间':'3min'}
#     return render_template('index.html', var = time, list = name, task = task )

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/result', methods=['POST', 'GET'])
def result1():
    if request.method == 'POST':
        result = request.form
        return render_template('result.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)  # 启动服务器， 并开启debug模式
