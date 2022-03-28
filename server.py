from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if(request.method == 'GET'):
        data = "Bienvenue dans mon service"
        return jsonify({'data': data})


@app.route('/receive/<string:temperature>/<string:moisture>', methods=['POST','GET'])
def receiveData(temperature,moisture):
    """"save to the database """
    return jsonify({
        'temperature': float(temperature),
        'moisture': float(moisture)
    })


if __name__=='__main___':
    app.run(debug=True)