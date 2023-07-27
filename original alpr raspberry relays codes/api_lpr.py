# Write your code here :-)
from flask import Flask, jsonify, request
import  json
import Motor_Final



app = Flask(__name__)



@app.route('/')
def hello():
    # return ' json api test'
    return jsonify({'name':'Deha',
                    'address':'test data'})

@app.route('/Open')
def OpennClose():
    # return ' json api test'
    Motor_Final.open()
    return jsonify({'status':'done'
                    })

#app.run()
app.run(debug=True, port=5000, host='0.0.0.0')