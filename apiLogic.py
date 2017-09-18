from apiModel.reportModel import Report
from apiModel.keywordModel import Keyword, KeywordSchema
from apiModel.valueModel import Value
from predictionModel import PredictionModel
from dataAccess import DataAccess
from itertools import groupby
from trainingModel import TrainingModel
from os import listdir
import jieba
import re
from chinese_digit import ChineseDigit
import csv
# import numpy

class ApiLogic:
    def getAvailableReports(self, subject):
        return self.getIdAndNames(subject)

    def __init__(self, testMode = False):
        self._testMode = testMode
        self.__subject_report_type_mapping = {'finance': 'annual-reports', 'law': 'law-verdicts'}

    # For now, we only have a single keyword: Total Revenue. This method will need to be refactored once more keywords are added.
    def getReportByID(self, id, subject = 'Fiance'):
        dataAccess = DataAccess(subject = subject)
        return dataAccess.getReportByID(id)
        # reportRaw = dataAccess.getReportByID(id)
        # if reportRaw != None:
        #     report = Report()
        #     report.id = id
        #     report.name = reportRaw.name
        #     report.keywords = reportRaw.keywords
            # report.keywords = []

            # reportType = 'form-10-k-annual-reports' if reportRaw.is10K == 'TRUE' else 'non-form-10-k-annual-reports'
            # predictResult = reportRaw.predictResult
            # values = []
            # if (predictResult != None):
            #     # for r in predictResult:
            #     #     value = Value(r.page_number, r.line_number if r.line_number != None else -1, 'green' if r.line_number!= None else 'orange', r.line_text if r.line_number != None else r.page_text, r.keyword)
            #     #     keyword = value.keyword
            #     values = list(map(lambda r: Value(r.page_number, r.line_number if r.line_number != None else -1, 'green' if r.line_number!= None else 'orange', r.line_text if r.line_number != None else r.page_text, '', r.keyword), predictResult))
            #     keywordGroups = groupby(sorted(values, key=lambda x: x.keyword), lambda x: x.keyword)
            #     for keywordName, vIter in keywordGroups:
            #         keyword = Keyword()
            #         keyword.keyword = keywordName
            #         keyword.values = list(vIter)
            #         report.keywords.append(keyword)
                # test = list(map(lambda r: r['page_number'], predictResult))

            # totalRevenueKeyword = Keyword()
            # totalRevenueKeyword.keyword = 'Total Revenue'
            # #totalRevenueKeyword.values = [Value(3, 5, 'Green', '$1000'), Value(5, 6, 'Green', '$2000')]
            # totalRevenueKeyword.values = values
            # report.keywords.append(totalRevenueKeyword)
            # totalAssetsKeyword = Keyword()
            # return report
        # name10KPair = self.getNameAndIsForm10KByID(id)
        # if name10KPair != None:
        #     reportType = 'form-10-k-annual-reports' if name10KPair[1] else 'non-form-10-k-annual-reports'
        #     predictionModel = PredictionModel(name10KPair[0], reportType)
        #     predictResult = predictionModel.predictTotalRevenue()
        #     #values = list(map(lambda r: Value(r['page_number'], r['line_number'], 'green', r['line_text']), predictResult))
        #     values = list(map(lambda r: Value(r['page_number'], r['line_number'] if 'line_number' in r else -1, 'green' if 'line_number' in r else 'orange', r['line_text'] if 'line_number' in r else r['page_text']), predictResult))
        #     #test = list(map(lambda r: r['page_number'], predictResult))
        #     report = Report()
        #     report.id = id
        #     report.name = name10KPair[0]
        #     report.keywords = []
        #     totalRevenueKeyword = Keyword()
        #     totalRevenueKeyword.keyword = 'Total Revenue'
        #     #totalRevenueKeyword.values = [Value(3, 5, 'Green', '$1000'), Value(5, 6, 'Green', '$2000')]
        #     totalRevenueKeyword.values = values
        #     report.keywords.append(totalRevenueKeyword)
        #     return report

    # Returns a tuple. First element is name of the report. Second element is True/False indicating whether the report is in Form 10K.
    def getNameAndIsForm10KByID(self, id):
        idStr = str(id)
        mapFile = open("id-name-map.txt", encoding="utf8")
        mapLines = mapFile.readlines()
        line = list(filter(lambda l: l.split(',')[0] == idStr, mapLines))
        mapFile.close()
        if line.__len__() > 0:
            splited = line[0].split(',')
            name = splited[2].rstrip()
            isForm10 = True if splited[1] == 'TRUE' else False
            return (name, isForm10)
        return None

    # We may need to move this to a specific file. This method is for searching verdicts by person and company name.
    def search_verdicts(self, person_name, company_name):
        person_name = '被告人' + person_name
        dataAccess = DataAccess(subject = 'law')
        all_reports = dataAccess.getIdAndNames()
        result = []
        for report in all_reports:
            folder_path = "documents-convert\\paragraphs-law-verdicts\\" + report['name']
            file_name_list = listdir(folder_path)
            name_found = False
            company_found = False
            for file_name in file_name_list:
                with open(folder_path + '\\' + file_name, mode='r', encoding='utf-8') as file:
                    content = file.read()
                    if person_name in content and report not in result:
                        name_found = True
                        if company_name in content:
                            company_found = True
            if name_found == True:
                report['matching'] = 100 if company_found == True else 50
                result.append(report)
        result.sort(key=lambda r: float(r['matching']), reverse=True)
        # mean_matching = numpy.mean(list(r['matching'] for r in result))
        # mean_score = numpy.mean(list(float(r['reportScore']) for r in result))
        return result



    def trainModels(self):
        tm = TrainingModel(page_keyword = 'Income Statements', line_keyword = 'Total Revenues')
        tm.train()
        tm = TrainingModel(page_keyword = 'Balance Sheets', line_keyword = 'Total Assets')
        tm.train()
        tm = TrainingModel(paragraph_keyword = 'Law Verdicts', encoding = 'utf-8', binary = True, tokenizer = jieba.cut, model = 'linear_svc')
        tm.train()

    def getIdAndNames(self, subject):
        dataAccess = DataAccess(subject = subject)
        return dataAccess.getIdAndNames()
        # mapFile = open("id-name-map.txt", encoding="utf8")
        # mapLines = mapFile.readlines()
        # result = list(map(lambda l: {"id": l.split(',')[0], "name": l.split(',')[2].rstrip()}, mapLines))
        # mapFile.close()
        # return result

    def pridictSingleReport(self, id, subject):
        dataAccess = DataAccess(subject = subject)
        report = dataAccess.getReportByID(id)
        name = report.name
        if subject == 'finance':
            predictionModel = PredictionModel(name, 'annual-reports')
            predictResult = predictionModel.predict([('Income Statements', 'Total Revenue', ''), ('Balance Sheets', 'Total Assets', '')])
            consolidated = self._consolicate_keywords(predictResult, ['Total Revenues', 'Total Assets'], subject)
        if subject == 'law':
            predictionModel = PredictionModel(name, 'law-verdicts', encoding = 'utf-8', binary = True, tokenizer = jieba.cut, model = 'linear_svc')
            predictResult = predictionModel.predict([('', '', 'Law Verdicts')])
            consolidated = self._consolicate_keywords(predictResult, ['Law Verdicts'], subject)
        keywordsRaw = []
        for keyword in consolidated[0]:
            keywordsRaw.append(dict(keyword))
        score_rule = consolidated[2] if len(consolidated) > 2 else ''
        dataAccess.savePredictResult(id, predictResult, keywordsRaw, consolidated[1], score_rule)

    def pridictAllReports(self, subject = 'Finance'):
        dataAccess = DataAccess(subject = subject)
        idNames = dataAccess.getIdAndNames()
        for pair in idNames:
            try:
                id = pair['id']
                name = pair['name']
                if self._testMode:
                    print(name)
                if subject == 'finance':
                    predictionModel = PredictionModel(name, 'annual-reports')
                    predictResult = predictionModel.predict(
                        [('Income Statements', 'Total Revenue', ''), ('Balance Sheets', 'Total Assets', '')])
                    consolidated = self._consolicate_keywords(predictResult, ['Total Revenues', 'Total Assets'], subject)
                if subject == 'law':
                    predictionModel = PredictionModel(name, 'law-verdicts', encoding='utf-8', binary=True, tokenizer=jieba.cut, model='linear_svc')
                    predictResult = predictionModel.predict([('', '', 'Law Verdicts')])
                    consolidated = self._consolicate_keywords(predictResult, ['Law Verdicts'], subject)
                keywordsRaw = []
                for keyword in consolidated[0]:
                    keywordsRaw.append(dict(keyword))
                score_rule = consolidated[2] if len(consolidated) > 2 else ''
                dataAccess.savePredictResult(id, predictResult, keywordsRaw, consolidated[1], score_rule)
            except Exception as e:
                print(e)
                continue

    def _consolicate_keywords(self, predictResult, requiredKeywords, subject='Finance'):
        if subject == 'finance':
            return self._consolicate_general_keywords(predictResult, requiredKeywords)
        if subject == 'law':
            return self._consolicate_law_keywords(predictResult, requiredKeywords)

    # Turn prediction result into front-end friendly format. And calculate a score for each keyword and the whole report.
    # Returns a tuple. First element is a list of keywords. Second element is report's total score.
    def _consolicate_general_keywords(self, predictResult, requiredKeywords):
        # Keyword score calculation rule:
        # Full Score: 90
        # No value found: 0
        # For each value:
            # Value score = Full Score / n (number of values)
            # If line found: Value full score achieved
            # If only page found: Value full score / 2
        # Sum each value's score to obtain achieved_score.
        # If a single value is found, full score is achieved. If 2 values are found, minus 10. If 3 values are found, minus 20, and so on… Formula:
            # Achieved score – (n – 1) * 10
        # Report score is the average of all keywords.

        keywords = []
        full_score = 90
        # values = list(map(lambda r: Value(r['page_number'], r['line_number'] if 'line_number' in r else -1,
        #                                   'green' if 'line_number' in r else 'orange',
        #                                   r['line_text'] if 'line_number' in r else 'You can find ' + r['keyword'] + ' on page ' + str(r['page_number']) + '.', '', r['keyword'],'lines' if 'line_number' in r else 'pages'),

        values = list(map(lambda r: Value(page = r['page_number'] if 'page_number' in r else '-1',
                                          line = r['line_number'] if 'line_number' in r else -1,
                                          color = 'green' if 'line_number' in r else 'orange',
                                          textToHighlight = r['line_text'] if 'line_number' in r else 'You can find ' + r['keyword'] + ' on page ' + str(r['page_number']) + '.' if 'page_number' in r else '',
                                          keyword = r['keyword'],
                                          type = 'lines' if 'line_number' in r else 'pages'),
                          predictResult))
        keywordGroups = groupby(sorted(values, key=lambda x: x.keyword), lambda x: x.keyword)
        report_score = 0
        for keywordName, vIter in keywordGroups:
            keyword = Keyword()
            keyword.keyword = keywordName
            keyword.values = list(vIter)
            if len(keyword.values) == 0:
                keyword.score = '0'
            else:
                value_score = full_score / len(keyword.values)
                achieved_score = 0
                for value in keyword.values:
                    achieved_score += value_score / 2 if value.line == -1 else value_score
                final_score = achieved_score - (len(keyword.values) - 1) * 10
                keyword.score = str(final_score)
                report_score += final_score
            keywords.append(keyword)
        # Add missing keywords with empty values.
        keywordNames = list(map(lambda k:k.keyword, keywords))
        for requiredKeyword in requiredKeywords:
            if requiredKeyword not in keywordNames:
                addKey = Keyword()
                addKey.keyword = requiredKeyword
                addKey.values = []
                addKey.score = '0'
                keywords.append(addKey)
        report_score /= len(keywords)
        report_score = round(max(0, report_score), 2)
        return (keywords, str(report_score))

    # Read crime scores from crime_score.csv
    def _consolicate_law_keywords(self, predictResult, requiredKeywords):
        # crime_scores = {'危险驾驶': 5,
        #                 '盗窃': 10,
        #                 '职务侵占': 20,
        #                 '虚报注册资本': 30,
        #                 '走私': 40,
        #                 '行贿' : 50,
        #                 '受贿': 60,
        #                 '贪污': 70,
        #                 '金融诈骗': 80,
        #                 '伪造货币': 90,
        #                 '叛国': 100}
        reader = csv.reader(open('configurations\\crime_score.csv', 'r', encoding='utf-8'))
        crime_scores = {}
        for i, line in enumerate(reader):
            if i != 0:
                crime_scores[line[0]] = int(line[1])
        keywords = []
        report_score = 0
        crime_count = 0
        crime_score = 0
        verdict_type = ''
        verdict_count = 0
        verdict_score = 0
        crime_type = ''
        score_rule = '分数分为罪行分和判刑分两种，总分为罪行分*0.6+判刑分*0,4。该被告犯{0}罪，罪行分{1}分，判刑为{2}，判刑分{3}分，总分{1}*0.6+{3}*0.4={4}分。'
        values = list(map(lambda r: Value(color = 'green', textToHighlight = r['paragraph_text'], keyword = r['keyword'],
                                          type = 'paragraphs', paragraph = r['paragraph_number']),
                          predictResult))
        for value in values:
            # Crime score.
            for crime, score in crime_scores.items():
                if crime in value.textToHighlight:
                    crime_type = crime
                    crime_score += score
                    crime_count += 1
                    break
            # Verdict score.
            if '死刑' in value.textToHighlight:
                verdict_type = '死刑'
                verdict_score += 100
                verdict_count += 1
            elif '无期徒刑' in value.textToHighlight:
                verdict_type = '无期徒刑'
                verdict_score += 70
                verdict_count += 1
            else:
                verdict_year = self.consolidate_verdict_score(r'有期徒刑(.*?)年', value.textToHighlight)
                if verdict_year > 0:
                    verdict_type = '有期徒刑' + str(verdict_year) + '年'
                    verdict_score += verdict_year * 2
                    verdict_count += 1
            if crime_count > 0 and verdict_count > 0:
                break

        keywordGroups = groupby(sorted(values, key=lambda x: x.keyword), lambda x: x.keyword)

        for keywordName, vIter in keywordGroups:
            keyword = Keyword()
            keyword.keyword = keywordName
            keyword.score = '0'
            keyword.values = list(vIter)
            keywords.append(keyword)

        # Add missing keywords with empty values.
        keywordNames = list(map(lambda k:k.keyword, keywords))
        for requiredKeyword in requiredKeywords:
            if requiredKeyword not in keywordNames:
                addKey = Keyword()
                addKey.keyword = requiredKeyword
                addKey.values = []
                addKey.score = '0'
                keywords.append(addKey)
        if crime_count > 0:
            crime_score /= crime_count
        if verdict_count > 0:
            verdict_score /= verdict_count
        report_score = crime_score * 0.6 + verdict_score * 0.4
        score_rule = score_rule.format(crime_type, crime_score, verdict_type, verdict_score, report_score)
        return (keywords, str(report_score), score_rule)

    def consolidate_verdict_score(self, crime_re, text):
        re_result = re.findall(crime_re, text)
        if len(re_result) > 0:
            chinese_digit = ChineseDigit()
            return chinese_digit.getResultForDigit(re_result[-1])
        return 0

# Tests
# al = ApiLogic(False)
# al.trainModels()
# al.pridictAllReports('law')
# al.pridictSingleReport('599266678faeae40e07c905a', 'law')

# al = ApiLogic(False)
# print(al.search_verdicts('吴进宝', '岳阳监狱十二监区副监区长'))


