from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)

WORK_FOLDER = 'receive'


@app.route('/hello')
def hello_world():
    return "hello world"

@app.route('/upload', methods=['POST'])
def upload():
    # 读取post body 里面的 file
    f = request.files['data']
    print(f.filename)
    # 将 file 写入文件
    now = time.strftime("%y-%m-%d%H%M%S",time.localtime(time.time()))
    print(now)
    newName = WORK_FOLDER + '/' + now + secure_filename(f.filename[-10:]) 
    f.save(newName)
    insert_imgs(newName)

    # 返回成功的函数
    return jsonify({'msg': 'success'}), 200 # http状态码

import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='test',
    port=3306)

# fp = open('./receive/wxe0033f9a4eca176d.o6zAJs8lOPR_EiprRvKX_2ixMHrQ.Zusfsb9c8XmY1080578deb95d5f64bf19300cd4ff3db.jpg')
# img = fp.read
# fp.close()

def insert_imgs(filename):
    cur = db.cursor()
    cur.execute("Insert into pictures(picaddr) values(%s)", (filename))
    db.commit()
    cur.close()
    db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
