from pymongo import MongoClient
from apiModel.reportModel import ReportSchema
from bson.objectid import ObjectId
from os import stat
import pandas

class DataAccess:
    def __init__(self, testMode = False, subject = 'finance'):
        self._testMode = testMode
        if testMode == True:
            client = MongoClient()
        else:
            uri = "report-reader.southeastasia.cloudapp.azure.com:27017"
            client = MongoClient(uri)
            # client = MongoClient()
        self._database = client['report-reader-database']
        self._collection = self._database['reports']
        subject = subject.lower()
        if subject == 'finance':
            self._collection = self._database['reports']
        if subject == 'law':
            self._collection = self._database['verdicts']
        if subject == 'hr':
            self._collection = self._database['candidates']
        self._subject = subject

    def getIdAndNames(self):
        report_list = []
        # for report in self._collection.find({}, {'_id': 1, 'name': 1, 'size': 1, 'reportScore': 1}):
        for report in self._collection.find({}, {'_id': 1, 'name': 1, 'size': 1, 'reportScore': 1, 'completionRate': 1}):
        # for report in self._collection.find({'name': {'$regex': '.*Test.*'}}, {'_id': 1, 'name': 1, 'size': 1, 'reportScore': 1, 'completionRate': 1}):
            report.update({"id": str(report["_id"])})
            del report["_id"]
            report_list.append(report)
        return report_list

    def getIds(self):
        report_list = []
        for report in self._collection.find({}, {'_id': 1}):
            report.update({"id": str(report["_id"])})
            del report["_id"]
            report_list.append(report)
        return report_list

    def getAll(self):
        report_list = []
        for report in self._collection.find({}):
            report.update({"id": str(report["_id"])})
            del report["_id"]
            report_list.append(report)
        return report_list

    def getReportByID(self, id):
        report = self._collection.find_one({"_id": ObjectId(id)})
        reportSchema = ReportSchema(strict = True)
        return reportSchema.load(report).data

    def savePredictResult(self, id, predictResult, keywords, reportScore, scoreRule = ''):
        report = self._collection.update_one(
            {"_id": ObjectId(id)},
            {'$set': {
                'predictResult': predictResult,
                'keywords': keywords,
                'reportScore': reportScore,
                'completionRate': '0', # Change this to the actual value later.
                'scoreRule': scoreRule
            }})

    def import_single_report(self, name):
        file_info = stat("static\\PDFJS\\PDF\\" + name + '.pdf')
        file_size_bytes = file_info.st_size
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if file_size_bytes < 1024.0:
                file_size_format = "%3.1f %s" % (file_size_bytes, unit)
                break
            file_size_bytes /= 1024.0
        self._collection.insert_one({"name": name, "size": file_size_format})

    def import_new_candidates(self):
        df = pandas.read_csv('documents-convert\\ConsolidatedCandidates.csv')
        dict_list = df.to_dict('records')
        for dict in dict_list:
            self.transform_work_experience(dict, 'RecentJob')
            self.transform_work_experience(dict, 'HistoryJob1')
            self.transform_work_experience(dict, 'HistoryJob2')
            dict['JobHistory'] = [dict['RecentJob'], dict['HistoryJob1'], dict['HistoryJob2']]
            dict['JobHistory'] = list(filter(lambda h: str(h['Position']) != 'nan', dict['JobHistory']))
            del dict['RecentJob']
            del dict['HistoryJob1']
            del dict['HistoryJob2']
            dict['ExpectedSalary'] = { 'LowerLimit': dict['ExpectedSalary.LowerLimit'], 'UpperLimit':  dict['ExpectedSalary.UpperLimit'] }
            del dict['ExpectedSalary.LowerLimit']
            del dict['ExpectedSalary.UpperLimit']
        self._collection.insert(dict_list)


    def transform_work_experience(self, dict, work_name):
        dict[work_name] = {'Position': dict[work_name + '.Position'], 'Firm': dict[work_name + '.Firm'],
                             'StartDate': dict[work_name + '.StartDate'], 'EndDate': dict[work_name + '.EndDate'],
                             'Months': dict[work_name + '.Months']}
        del dict[work_name + '.Position']
        del dict[work_name + '.Firm']
        del dict[work_name + '.StartDate']
        del dict[work_name + '.EndDate']
        del dict[work_name + '.Months']

# Tests.
# from predictionModel import PredictionModel
#
# da = DataAccess(False)
# da.import_single_report('[Test]Apple_Annual_Report_2016_Form_10-K')
# ###da.getIdAndNames()
# ###da.insertInitialData()
# id = '596722f8f1156f1aa8fc56a2'
# da.getReportByID(id)
# report = da.getReportByID(id)
# reportType = 'form-10-k-annual-reports'
# predictionModel = PredictionModel(report.name, reportType)
# predictResult = predictionModel.predict([('Income Statements', 'Total Revenue'), ('Balance Sheets', 'Total Assets')])
# da.savePredictResult(id, predictResult)
