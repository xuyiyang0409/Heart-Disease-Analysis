from flask import Flask
from flask_restplus import fields, Api, Resource
from flask_cors import CORS
import re
import sys
sys.path.append('../')

from backend.db_handler import DBHandler
from machine_learning import multi_classification, feature_selection

app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app, title="Heart Disease", description="API for Heart Disease Analysis, Group Master Branch")
db_controller = DBHandler()


attr_parser = api.parser()
attr_parser.add_argument('name', type=str, help='Request your attribute name here', location='args')


@api.route('/attr')
@api.doc(parser=attr_parser)
@api.response(200, 'OK')
@api.response(400, 'Bad Request')
@api.response(404, 'Not Found')
class Attributes(Resource):
    def get(self):
        attribute_name = attr_parser.parse_args()['name']

        if not attribute_name:
            return {"Please ensure you provide a coordinate!"}, 400

        result = db_controller.database_controller(f"SELECT age, sex, {attribute_name} FROM Rawdata;")
        if not result:
            return {"message": f"{attribute_name} not found in database!"}, 404

        return {
            f"{attribute_name}": result
        }, 200


@api.route('/factor')
@api.response(200, 'OK')
@api.response(404, 'Not Found')
class Factors(Resource):
    def get(self):
        result = db_controller.database_controller("SELECT * FROM Impfactor")
        if not result:
            selecter = feature_selection.FeatureSelection()
            selecter.correlation()
            return {"message": "The important factors are not yet determined!"}, 404
        base_name = "importantFactor"
        result_dict = dict()
        for i in range(len(result[0])):
            result_dict[base_name + str(i + 1)] = result[0][i]
        return result_dict, 200


predict_parser = api.parser()
predict_parser.add_argument('type', type=int, help='Input prediction type', location='args')
payload_model = api.model('POST Payload',
                          {"ca": fields.String,
                           "oldpeak": fields.String,
                           "thalach": fields.String,
                           "cp": fields.String,
                           "exang": fields.String
                           })


@api.route('/predict')
@api.doc(parser=predict_parser)
@api.response(200, 'OK')
@api.response(400, 'Bad Request')
@api.response(404, 'Not Found')
class Predict(Resource):
    @api.expect(payload_model)
    def post(self):
        predict_type = predict_parser.parse_args()['type']
        if not predict_type or predict_type not in {1, 2}:
            return {"message": "Bad Request, please check your argument is either 1 or 2!"}, 400

        if not api.payload:
            return {"message": "Bad Request, please check your payload format!"}, 400

        predict_value = {"ca": None,
                         "oldpeak": None,
                         "thalach": None,
                         "cp": None,
                         "exang": None}

        binary_result_map = {0: "No Disease",
                             1: "may have heart disease"}

        multi_result_map = {0: "No Disease",
                            1: "may have heart disease, Level 1",
                            2: "may have heart disease, Level 2",
                            3: "may have heart disease, Level 3",
                            4: "may have heart disease, Level 4"}

        for i in api.payload:
            if i not in predict_value.keys():
                return {"message": f"{i} is not an important factor!"}, 404
            predict_value[i] = float(api.payload[i])

        if predict_type == 1:
            binary_classify = db_controller.database_controller(f"SELECT * FROM Predict;")
            impfactor1 = binary_classify[0]
            impfactor2 = binary_classify[1]
            impfactor3 = binary_classify[2]
            impfactor4 = binary_classify[3]
            impfactor5 = binary_classify[4]
            constant = binary_classify[5]
            value1 = predict_value['ca']
            value2 = predict_value["oldpeak"]
            value3 = predict_value["thalach"]
            value4 = predict_value["cp"]
            value5 = predict_value["exang"]
            result = impfactor1 * value1 + impfactor2 * value2 + impfactor3 * value3 +\
                     impfactor4 * value4 + impfactor5 * value5 + constant
            return {"message": binary_result_map[result],
                    "level": f"{result}"}, 200

        if predict_type == 2:
            multi_classify = multi_classification.MultiClassifier()
            result = multi_classify.predict(predict_value)
            return {"message": multi_result_map[result],
                    "level": f"{result}"}, 200


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8888, debug=True)
