from flask import Flask, request, jsonify,send_from_directory
from werkzeug.utils import secure_filename
import time
import requests
import json
import os
import pymysql

app = Flask(__name__)
appid = 'wx6a9e1b45192f6be1'
secret = '54fde56821165571f875674242d23108'
WORK_FOLDER = 'receive'

sql1 = "Select ID from uid where wechatID = %s"#openid替换成系统id
sql2 = "Insert into uid(wechatID) select %s from dual where not exists (select * from uid where wechatID = %s)"#重复账户检测
sql3 = "select id, picaddr, time from pictures order by time desc"
sql4 = "select ID from uid where wechatID = %s"

@app.route('/hello')
def hello_world():
    return "hello world"

@app.route('/code', methods=['GET', 'POST'])
def getuserinfo():
    data = json.loads(request.data)
    code = data['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (appid, secret, code)
    r = requests.get(url)
    print(r.text)
    result = json.loads(r.text)
    print(result['openid'])
    cur = db.cursor()
    db.ping(reconnect=True)
    cur.execute(sql2,(result['openid'],result['openid']))#查询是否为新用户并插入新用户到用户表uid
    cur.execute(sql4,result['openid'])
    b =cur.fetchone()
    print(b[0])
    db.commit()
    cur.close()
    db.close()
    rd = {'name':[]}
    rd['name'].append({'openid': result['openid'],'id':b[0]})
    print(rd)
    return jsonify(rd)

@app.route('/upload', methods=['POST'])
def upload():
    # 读取post body 里面的 file
    f = request.files['data']
    n = request.form['oid']
    print(f.filename)
    # 将 file 写入文件
    now = time.strftime("%y-%m-%d%H%M%S",time.localtime(time.time()))
    newName = WORK_FOLDER + '/' + now + secure_filename(f.filename[-10:])
    print(newName) 
    f.save(newName)
    insert_imgs(n,newName,now)

    # 返回成功的函数
    return jsonify({'msg': 'success'}), 200 # http状态码

@app.route("/shareshow", methods=['GET'])#将图片上传者及图片地址以字典形式发送给前端
def shareShow1():
    db = pymysql.connect("localhost", "root", "123456", "test")
    cursor = db.cursor()
    try:
        cursor.execute(sql3)
        temp = cursor.fetchall()
        db.commit()
    except:
        db.rollback()
    db.close()
    re = {'list': []}
    for i in range(len(temp)):
        re['list'].append({'id': temp[i][0], 'picaddr': temp[i][1],'time':temp[i][2]})
    return jsonify(re)

@app.route("/shareshow/<path:sharePath>") #返回图片内容并在前端显示
def shareShow2(sharePath):
    return send_from_directory('',sharePath,as_attachment=True)


db = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='test',
    port=3306)

# fp = open('./receive/wxe0033f9a4eca176d.o6zAJs8lOPR_EiprRvKX_2ixMHrQ.Zusfsb9c8XmY1080578deb95d5f64bf19300cd4ff3db.jpg')
# img = fp.read
# fp.close()



def insert_imgs(num,filename,moment):
    cur = db.cursor()
    cur.execute(sql1,num)
    a = cur.fetchone()
    print(a[0])

    cur.execute("Insert into pictures(id,wechatID,picaddr,time) values(%s, %s, %s, %s)", (int(a[0]), num, filename, moment)) #, (9,str(num),filename,moment)
    db.commit()
    cur.close()
    db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
