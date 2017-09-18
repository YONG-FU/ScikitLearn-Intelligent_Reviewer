from marshmallow import Schema, fields, post_load

class PredictResult:
    def __init__(self, keyword = '', page_path = '', page_number = '', page_text = '', line_number = '', line_text = '', paragraph_number = '', paragraph_text = ''):
        self.keyword = keyword
        self.page_path = page_path
        self.page_number = page_number
        self.page_text = page_text
        self.line_number = line_number
        self.line_text = line_text
        self.paragraph_number = paragraph_number
        self.paragraph_text = paragraph_text

    @property
    def keyword(self):
        return self.__keyword

    @keyword.setter
    def keyword(self, val):
        self.__keyword = val

    @property
    def page_path(self):
        return self.__page_path

    @page_path.setter
    def page_path(self, val):
        self.__page_path = val

    @property
    def page_number(self):
        return self.__page_number

    @page_number.setter
    def page_number(self, val):
        self.__page_number = val

    @property
    def page_text(self):
        return self.__page_text

    @page_text.setter
    def page_text(self, val):
        self.__page_text = val

    @property
    def line_number(self):
        return self.__line_number

    @line_number.setter
    def line_number(self, val):
        self.__line_number = val

    @property
    def line_text(self):
        return self.__line_text

    @line_text.setter
    def line_text(self, val):
        self.__line_text = val

    @property
    def paragraph_number(self):
        return  self.__paragraph_number

    @paragraph_number.setter
    def paragraph_number(self, val):
        self.__paragraph_number = val

    @property
    def paragraph_text(self):
        return  self.__paragraph_text

    @paragraph_text.setter
    def paragraph_text(self, val):
        self.__paragraph_text = val

class PredictResultSchema(Schema):
    keyword = fields.Str()
    page_path = fields.Str()
    page_number = fields.Integer()
    page_text = fields.Str()
    line_number = fields.Integer()
    line_text = fields.Str()
    paragraph_number = fields.Integer()
    paragraph_text = fields.Str()

    @post_load
    def makePredictResult(self, data):
        return PredictResult(**data)
