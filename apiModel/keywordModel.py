from .valueModel import Value, ValueSchema
from marshmallow import Schema, fields, post_load

# Model for a keyword.
class Keyword:
    def __init__(self, keyword = '', values = None, score = None):
        self.keyword = keyword
        self.values = values
        self.score = score

    @property
    def keyword(self):
        return self.__keyword

    @keyword.setter
    def keyword(self, val):
        self.__keyword = val

    @property
    def values(self):
        return self.__values

    @values.setter
    def values(self, val):
        self.__values = val

    @property
    def score(self):
        return  self.__score

    @score.setter
    def score(self, val):
        self.__score = val

    def __iter__(self):
        yield 'keyword', self.keyword
        yield 'values', list(map(lambda v: dict(v), self.values))
        yield 'score', self.score

class KeywordSchema(Schema):
    keyword = fields.Str()
    values = fields.Nested("ValueSchema", many = True)
    score = fields.Str()

    @post_load
    def makeKeyword(self, data):
        return Keyword(**data)