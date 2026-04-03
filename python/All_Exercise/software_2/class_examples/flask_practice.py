# from flask import Flask,request
#
# app = Flask(__name__)
# @app.route('/sum')
# def calculate_sum():
#     args = request.args
#     number1 = float(args.get("number1"))
#     number2 = float(args.get("number2"))
#     total_sum = number1+number2
#     return str(total_sum)
#
# if __name__ == '__main__':
#     app.run(use_reloader=True, host='127.0.0.1', port=5000)






# from flask import Flask, request
#
# app = Flask(__name__)
# @app.route('/sum')
# def calculate_sum():
#     args = request.args
#     number1 = float(args.get("number1"))
#     number2 = float(args.get("number2"))
#     total_sum = number1+number2
#
#     response = {
#         "number1" : number1,
#         "number2" : number2,
#         "total_sum" : total_sum
#     }
#
#     return response
#
# if __name__ == '__main__':
#     app.run(use_reloader=True, host='127.0.0.1', port=5000)










# from flask import Flask
#
# app = Flask(__name__)
# @app.route('/echo/<text>')
# def echo(text):
#     response = {
#         "echo" : text + " " + text
#     }
#     return response
#
# if __name__ == '__main__':
#     app.run(use_reloader=True, host='127.0.0.1', port=3000)








import json

from flask import Flask, Response

app = Flask(__name__)
@app.route('/sum/<number1>/<number2>')
def calculate_sum(number1, number2):
    try:
        number1 = float(number1)
        number2 = float(number2)
        total_sum = number1+number2
        response = {
            "number1" : number1,
            "number2" : number2,
            "total_sum" : total_sum,
            "status" : 200
        }
        return response

    except ValueError:
        response = {
            "message": "Invalid number as addend",
            "status": 400
        }
        json_response = json.dumps(response)
        http_response = Response(response=json_response, status=400, mimetype="application/json")
        return http_response

@app.errorhandler(404)
def page_not_found(error_code):
    response = {
        "message": "Invalid endpoint",
        "status": 404
    }
    json_response = json.dumps(response)
    http_response = Response(response=json_response, status=404, mimetype="application/json")
    return http_response

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)

    # sum/10/20
    # dum/10/20
    # sum/10/2t0