from os import listdir
from re import findall
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.externals import joblib

class PredictionModel:
    # 定义基本属性
    report_name = ""
    report_type = ""

    # 定义私有属性：私有属性在类外部无法直接进行访问
    __page_keyword = ""
    __line_keyword = ""
    __pagePredictionModel = {}
    __linePredictionModel = {}

    # 定义构造方法
    def __init__(self, report_name, report_type, encoding = "utf-8", binary = False, tokenizer = None, model = 'linear_svc'):
        self.report_name = report_name
        self.report_type = report_type
        self.__encoding = encoding
        self.__tokenizer = tokenizer
        self.__binary = binary
        self.__model = model

    def __set_page_keyword(self, pageKeyword):
        self.__page_keyword = pageKeyword.lower().replace(' ', '-')

    def __set_line_keyword(self, lineKeyword):
        self.__line_keyword = lineKeyword.lower().replace(' ', '-')

    def __set_paragraph_keyword(self, paragraphKeyword):
        self.__paragraph_keyword = paragraphKeyword.lower().replace(' ', '-')

    def __initialise_prediction_model_common(self, datasets_categories, trained_model_path, customTokenizer = None):
        # 选取参与分析的文本类别

        # 从硬盘获取训练数据
        datasets_train = load_files('datasets-train',
                                    categories=datasets_categories,
                                    load_content=True,
                                    encoding=self.__encoding,
                                    decode_error='strict',
                                    shuffle=True, random_state=42)

        # 统计词语出现次数
        count_vectorizer = CountVectorizer(binary = self.__binary, tokenizer = self.__tokenizer)
        X_train_counts = count_vectorizer.fit_transform(datasets_train.data)

        # 使用tf-idf方法提取文本特征
        tfidf_transformer = TfidfTransformer()
        tfidf_transformer.fit_transform(X_train_counts)

        # 载入已经训练好的分类器
        clf = joblib.load(trained_model_path)
        return {"count_vectorizer": count_vectorizer, "tfidf_transformer": tfidf_transformer, "clf": clf}

    def __initialise_page_prediction_model(self):
        datasets_categories = ['target-pages-' + self.__page_keyword, 'non-target-pages-' + self.__page_keyword]
        trained_model_path = 'models-machine-learning\\' + self.__model + '_' + self.__page_keyword + '_pages.pkl'
        self._pagePredictionModel = self.__initialise_prediction_model_common(datasets_categories, trained_model_path)

    def __initialise_line_prediction_model(self):
        datasets_categories = ['target-lines-' + self.__line_keyword, 'non-target-lines-' + self.__line_keyword]
        trained_model_path = 'models-machine-learning\\' + self.__model + '_' + self.__line_keyword + '_lines.pkl'
        self._linePredictionModel = self.__initialise_prediction_model_common(datasets_categories, trained_model_path)

    def __initialise_paragragh_prediction_model(self):
        datasets_categories = ['target-paragraphs-' + self.__paragraph_keyword, 'non-target-paragraphs-' + self.__paragraph_keyword]
        trained_model_path = 'models-machine-learning\\' + self.__model + '_' + self.__paragraph_keyword + '_paragraphs.pkl'
        self._paragraphPredictionModel = self.__initialise_prediction_model_common(datasets_categories, trained_model_path)

    def __predict_page_result(self, page_text):
        # 预测用的新字符串
        docs_new = [page_text]

        # 字符串向量化处理
        X_new_counts = self._pagePredictionModel["count_vectorizer"].transform(docs_new)
        X_new_tfidf = self._pagePredictionModel["tfidf_transformer"].transform(X_new_counts)

        # 进行机器学习预测
        predicted = self._pagePredictionModel["clf"].predict(X_new_tfidf)
        return predicted[0]

    def __predict_line_result(self, line_text):
        # 预测用的新字符串
        docs_new = [line_text]

        # 字符串向量化处理
        X_new_counts = self._linePredictionModel["count_vectorizer"].transform(docs_new)
        X_new_tfidf = self._linePredictionModel["tfidf_transformer"].transform(X_new_counts)

        # 进行机器学习预测
        predicted = self._linePredictionModel["clf"].predict(X_new_tfidf)
        return predicted[0]

    def __predict_paragraph_result(self, paragraph_text):
        # 预测用的新字符串
        docs_new = [paragraph_text]

        # 字符串向量化处理
        X_new_counts = self._paragraphPredictionModel["count_vectorizer"].transform(docs_new)
        X_new_tfidf = self._paragraphPredictionModel["tfidf_transformer"].transform(X_new_counts)

        # 进行机器学习预测
        predicted = self._paragraphPredictionModel["clf"].predict(X_new_tfidf)
        return predicted[0]

    # Predict a single keyword. Each keyword contains a page and line part. E.g. page: Income Statements, line: Total Revenue.
    def predict_keyword_result(self, page_keyword, line_keyword, paragraph_keyword):
        predicted_keyword_result_list = []
        if page_keyword != '':
            self.__set_page_keyword(page_keyword)
            self.__initialise_page_prediction_model()
        if line_keyword != '':
            self.__set_line_keyword(line_keyword)
            self.__initialise_line_prediction_model()
        if paragraph_keyword != '':
            self.__set_paragraph_keyword(paragraph_keyword)
            self.__initialise_paragragh_prediction_model()

        # 读入需要分析预测的文件
        if page_keyword != '':
            folder_path = "documents-convert\\pages-" + self.report_type
        if paragraph_keyword != '':
            folder_path = "documents-convert\\paragraphs-" + self.report_type
        text_file_name_list = listdir(folder_path + "\\" + self.report_name)

        for file_name in text_file_name_list:
            with open(folder_path + "\\" + self.report_name + "\\" + file_name, encoding="utf8") as text_file_object:
                if text_file_object:
                    target_page_keyword_result_dictionary = {}
                    text = text_file_object.read()
                    if page_keyword != '':
                        predicted_page_result = self.__predict_page_result(text)
                        # 保存预测结果
                        if predicted_page_result == 1:
                            target_page_result_dictionary = {'keyword': line_keyword, "page_path": text_file_object.name, "page_number": int(text_file_object.name[-7:-5]), "page_text": text}
                            predicted_keyword_result_list.append(target_page_result_dictionary)

                    if paragraph_keyword != '':
                        predicted_paragraph_result = self.__predict_paragraph_result(text)
                        if predicted_paragraph_result == 1:
                            target_paragraph_result_dictionary = {'keyword': paragraph_keyword, "paragraph_path": text_file_object.name, "paragraph_number": int(text_file_object.name[-7:-5]), "paragraph_text": text}
                            predicted_keyword_result_list.append(target_paragraph_result_dictionary)

        if line_keyword != '' and len(predicted_keyword_result_list) == 1:
            with open(predicted_keyword_result_list[0]["page_path"], encoding="utf-8") as page_text_file_object:
                line_number = 0
                first_line_updated = False
                for line_text in page_text_file_object.readlines():
                    # total_revenue_pattern = "TOTAL|Total|total|REVENUE|Revenue|revenue|NET SALES|Net Sales|Net sales|Netsales|net sales|netsales"
                    # total_revenue_pattern_result = findall(total_revenue_pattern, line_text)

                    letter_pattern = "[A-Za-z]"
                    letter_pattern_result = findall(letter_pattern, line_text)
                    number_pattern = "[0-9]"
                    number_pattern_result = findall(number_pattern, line_text)

                    if len(letter_pattern_result) > 0 and len(number_pattern_result) > 0:
                        line_number = line_number + 1
                        predicted_line_result = self.__predict_line_result(line_text)

                        # 保存预测结果
                        if predicted_line_result == 1:
                            if (first_line_updated == False):
                                first_line_updated = True
                                predicted_keyword_result_list[0].update({'line_number': line_number, 'line_text': line_text})
                            else:
                                predicted_keyword_result_list.append({'keyword': predicted_keyword_result_list[0]['keyword'], 'page_path': predicted_keyword_result_list[0]['page_path'], 'page_number': predicted_keyword_result_list[0]['page_number'], 'page_text': predicted_keyword_result_list[0]['page_text'], 'line_number': line_number, 'line_text': line_text})

        return predicted_keyword_result_list

    # Predict a list of keywords.
    # The 'keywords' parameter is a list of tuples with 2 elements: pageKeyword and lineKeyword.
    def predict(self, keywords):
        resultList = []
        for keyword in keywords:
            partialResults = self.predict_keyword_result(keyword[0], keyword[1], keyword[2])
            resultList = resultList + partialResults
        return resultList

# Tests
# folder_path_lines = "documents-convert\\pages-form-10-k-annual-reports"
# lines_folder_name_list = listdir(folder_path_lines)
# for file_name in lines_folder_name_list:
#     print(file_name)
#     predictionModel = PredictionModel(file_name, 'form-10-k-annual-reports')
#     # predictResult = predictionModel.predict([('Income Statements', 'Total Revenue'), ('Balance Sheets', 'Total Assets')])
#     predictResult = predictionModel.predict([('Balance Sheets', 'Total Assets')])
#     for result in predictResult:
#         # print(result['keyword'])
#         print(result['page_number'])
#         print(result.get('line_number', ''))
#         print(result.get('line_text', ''))

# predictionModel = PredictionModel('Strayer_Education_Annual_Report_2016_Form_10-K', 'form-10-k-annual-reports')
# predictionModel.predict([('Income Statements', 'Total Revenue'), ('Balance Sheets', 'Total Assets')])