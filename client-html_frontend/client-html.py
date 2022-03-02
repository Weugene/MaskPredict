from flask import Flask, render_template, request
import requests
import logging
app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello', methods=['POST', 'GET'])
def hello():
    s = request.form['sentence']
    logging.critical('++++++text:'+s, exc_info=True)
    r = requests.post("http://server:1234/getmask", json=s)
    res = r.json()['result']
    resp = ''
    print(res)
    #return res[0]['MASK']
    for d in res:
        print(d['MASK'])
        print(d['weights:'])
        resp = resp + d['MASK'] + ":" + str(round(d['weights:'],2)) + ' <br>'
    #return resp
    return '<b>Answer:</b> <br> %s <br/> <a href="/">Back Home</a>' % (resp)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 4000)
