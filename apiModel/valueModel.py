from marshmallow import Schema, fields, post_load

# Model for a single value.
class Value:
    def __init__(self, page = 0, line = 0, paragraph = 0, color = '', textToHighlight = '', validationResult = '', keyword = '', type = ''):
        self.page = page
        self.line = line
        self.paragraph = paragraph
        self.color = color
        self.textToHighlight = textToHighlight
        self.validationResult = validationResult
        self.keyword = keyword
        self.type = type

    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, val):
        self.__page = val

    @property
    def line(self):
        return self.__line

    @line.setter
    def line(self, val):
        self.__line = val

    @property
    def paragraph(self):
        return self.__paragraph

    @paragraph.setter
    def paragraph(self, val):
        self.__paragraph  = val

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, val):
        self.__color = val

    @property
    def textToHighlight(self):
        return self.__textToHighlight

    @textToHighlight.setter
    def textToHighlight(self, val):
        self.__textToHighlight = val

    @property
    def validationResult(self):
        return self.__validationResult

    @validationResult.setter
    def validationResult(self, val):
        self.__validationResult = val

    @property
    def keyword(self):
        return self.__keyword

    @keyword.setter
    def keyword(self, val):
        self.__keyword = val

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, val):
        self.__type = val

    def __iter__(self):
        yield 'page', self.page
        yield 'line', self.line
        yield  'paragraph', self.paragraph
        yield 'color', self.color
        yield 'textToHighlight', self.textToHighlight
        yield 'validationResult', self.validationResult
        yield 'keyword', self.keyword
        yield 'type', self.type

class ValueSchema(Schema):
    page = fields.Integer()
    line = fields.Integer()
    paragraph = fields.Integer()
    color = fields.Str()
    textToHighlight = fields.Str()
    validationResult = fields.Str()
    keyword = fields.Str()
    type = fields.Str()

    @post_load
    def makeValue(self, data):
        return Value(**data)