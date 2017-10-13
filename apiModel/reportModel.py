from marshmallow import Schema, fields, post_load

# Model class for a report
class Report:
    def __init__(self, id = 0, name = '', keywords = None, is10K = 'TRUE', predictResult = None, reportScore = None, completionRate = '0', scoreRule = ''):
        self.id = id
        self.name = name
        self.keywords = keywords
        self.is10K = is10K
        self.predictResult = predictResult
        self.reportScore = reportScore
        self.completionRate = completionRate
        self.scoreRule = scoreRule

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, val):
        self.__id = val

    @property
    def is10K(self):
        return self.__is10K

    @is10K.setter
    def is10K(self, val):
        self.__is10K = val

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val):
        self.__name = val

    @property
    def keywords(self):
        return self.__keywords

    @keywords.setter
    def keywords(self, val):
        self.__keywords = val

    @property
    def predictResult(self):
        return self.__predictResult

    @predictResult.setter
    def predictResult(self, val):
        self.__predictResult = val

    @property
    def reportScore(self):
        return self.__reportScore

    @reportScore.setter
    def reportScore(self, val):
        self.__reportScore = val

    @property
    def completionRate(self):
        return self._completionRate

    @completionRate.setter
    def completionRate(self, val):
        self._completionRate = val

    @property
    def scoreRule(self):
        return self._scoreRule

    @scoreRule.setter
    def scoreRule(self, val):
        self._scoreRule = val

class ReportSchema(Schema):
    id = fields.Str()
    is10K = fields.Str()
    name = fields.Str()
    keywords = fields.Nested("KeywordSchema", many = True)
    predictResult = fields.Nested("PredictResultSchema", many = True)
    reportScore = fields.Str()
    completionRate = fields.Str()
    scoreRule = fields.Str()

    @post_load
    def makeReport(self, data):
        return Report(**data)