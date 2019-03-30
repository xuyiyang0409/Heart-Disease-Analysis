from flask import Flask
from flask_restplus import fields, Api, Resource
import re

from backend.db_handler import DBHandler

app = Flask(__name__)
api = Api(app, title="Heart Disease", description="API for Heart Disease Analysis, Group Master Branch")
db_controller = DBHandler()


parser = api.parser()
parser.add_argument('x', type=str, help='Request your x-coordinate here', location='args')
parser.add_argument('y', type=str, help='Request your y-coordinate here', location='args')


@api.route('/attr')
@api.doc(parser=parser)
@api.response(200, 'OK')
@api.response(400, 'Bad Request')
@api.response(404, 'Not Found')
class Attributes(Resource):
    def get(self):
        attribute_x = parser.parse_args()['x']
        attribute_y = parser.parse_args()['y']
        if not attribute_x or not attribute_y:
            return {"message": "Please ensure you provide both x and y coordinates!"}, 400

        result_x = db_controller.database_controller(f"SELECT {attribute_x} FROM Rawdata;")
        result_y = db_controller.database_controller(f"SELECT {attribute_y} FROM Rawdata;")
        if not result_x:
            return {"message": f"{attribute_x} not found in database!"}, 404
        if not result_y:
            return {"message": f"{attribute_y} not found in database!"}, 404

        return {
            "x": re.findall("\w+", str(result_x), flags=re.I),
            "y": re.findall("\w+", str(result_y), flags=re.I)
        }, 200


@api.route('/factor')
@api.response(200, 'OK')
@api.response(404, 'Not Found')
class Factors(Resource):
    def get(self):
        result = db_controller.database_controller("SELECT * FROM Impfactor")
        if not result:
            return {"message": "The important factors are not yet determined!"}, 404
        base_name = "importantFactor"
        result_dict = dict()
        for i in range(len(result[0])):
            result_dict[base_name + str(i + 1)] = result[0][i]
        return result_dict, 200


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8888, debug=True)