from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)
appid = 'wx6a9e1b45192f6be1'
secret = '54fde56821165571f875674242d23108'

@app.route('/code', methods=['GET', 'POST'])
def getuserinfo():
    data = json.loads(request.data)
    code = data['code']

    print(code)
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (appid, secret, code)
    print(url)
    r = requests.get(url)

    print(r.text)

    result = json.loads(r.text)

    print(result['openid'])
    # jRes = json.loads(result)
    return jsonify({'openid': result['openid']})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)