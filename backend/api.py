from flask import Flask
from flask_restplus import fields, Api, Resource
import re

from backend.db_handler import DBHandler

app = Flask(__name__)
api = Api(app, title="Heart Disease", description="API for Heart Disease Analysis, Group Master Branch")
db_controller = DBHandler()


parser = api.parser()
parser.add_argument('name', type=str, help='Request your name-coordinate here', location='args')

@api.route('/attr')
@api.doc(parser=parser)
@api.response(200, 'OK')
@api.response(400, 'Bad Request')
@api.response(404, 'Not Found')
class Attributes(Resource):
    def get(self):
        attribute_name = parser.parse_args()['name']

        if not attribute_name:
            return {"Please ensure you provide a coordinate!"}, 400

        result_name = db_controller.database_controller(f"SELECT age, sex, {attribute_name} FROM Rawdata;")
        # print(result_name)
        if not result_name:
            return {"message": f"{attribute_name} not found in database!"}, 404

        return {
            "f{attribute name}": f"{result_name}"
        }, 200
# re.findall("\w+", str(result_name), flags=re.I

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
