from predictionModel import PredictionModel
from generationDataset import GenerationDataset
from apiLogic import ApiLogic
from hrLogic import HRLogic
from apiModel.reportModel import ReportSchema
from OpenSSL import SSL
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/reports/', methods=['GET'])
def get_available_reports():
    # Cloud Connection Database
    # uri = "mongodb://report-reader:YxJvd4469TeDbZiqs4xQFNu7jUyZcJoYQK5bWnrCYEyyQ7TloOay3OYkqErfZ1DucHxo0T2Itha6cLSDH4ZLlQ==@report-reader.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
    # client = MongoClient(uri)
    #
    # # Local Connection Database
    # # client = MongoClient()
    #
    # database = client["report-reader-database"]
    # collection = database["reports"]
    # report_list = []
    # for report in collection.find({}, {'_id': 1, 'name': 1}):
    #     report.update({"id": str(report["_id"])})
    #     del report["_id"]
    #     report_list.append
    subject = request.args.get('subject').lower()
    report_list = []
    apiLogic = ApiLogic()
    if subject == 'hr':
        hrLogic = HRLogic()
        report_list = hrLogic.score_candidates()
    else:
        report_list = apiLogic.getAvailableReports(subject)
    return jsonify(report_list)

@app.route('/api/model/train', methods=['POST'])
def train_models():
    apiLogic = ApiLogic()
    apiLogic.trainModels()
    return 'Training completed.'

@app.route('/api/model/predict/<string:id>', methods=['POST'])
def pridictSingleReports(id):
    subject = request.args.get('subject').lower()
    apiLogic = ApiLogic()
    apiLogic.pridictSingleReport(id, subject)
    return  'Prediction completed.'

@app.route('/api/model/predict', methods=['POST'])
def pridictAllReports():
    apiLogic = ApiLogic()
    apiLogic.pridictAllReports()
    return  'Prediction completed.'

@app.route('/api/test/', methods=['GET'])
def test():
    reportName = "Adobe_Systems_Annual_Report_2016_Form_10-K"
    reportType = "annual-reports"
    predictionModel = PredictionModel(reportName, reportType)
    return jsonify(predictionModel.predict_keyword_result("Income Statements", "Total Revenue"))

@app.route('/api/reports/<string:id>', methods=['GET'])
def get_ml_results(id):
    subject = request.args.get('subject').lower()
    apiLogic = ApiLogic()
    apiLogic.pridictSingleReport(id, subject)
    mlResults = apiLogic.getReportByID(id, subject)
    reportSchema = ReportSchema()
    return reportSchema.dumps(mlResults)

@app.route('/api/feedback/', methods=["GET","POST"])
def process_feedback():
    feedback_json = request.get_json()
    generationDataset = GenerationDataset(feedback_json)
    generationDataset.generateData()
    return str(feedback_json)

@app.route('/api/verdicts/', methods=['GET'])
def search_verdicts():
    person_name = request.args.get('person_name')
    company_name = request.args.get('company_name')
    apiLogic = ApiLogic()
    return jsonify(apiLogic.search_verdicts(person_name, company_name))

if __name__ == '__main__':
    # host="0.0.0.0" make the operating system listen on a public IP across virtual machine network.
    # context = ('certificate.crt', 'certificate.key')
    app.run(threaded=True)