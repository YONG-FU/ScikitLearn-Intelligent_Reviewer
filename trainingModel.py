from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC, NuSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

class TrainingModel:
    def __init__(self, page_keyword = '', line_keyword = '', paragraph_keyword = '', encoding = 'latin1', binary = False, tokenizer = None, model = 'linear_svc'):
        self.__page_keyword = page_keyword.lower().replace(' ', '-')
        self.__line_keyword = line_keyword.lower().replace(' ', '-')
        self.__paragraph_keyword = paragraph_keyword.lower().replace(' ', '-')
        self.__encoding = encoding
        self.__tokenizer = tokenizer
        self.__binary = binary
        self.__model = model

    def __select_model(self):
        if self.__model == 'linear_svc':
            return LinearSVC()
        if self.__model == 'multinomial_nb':
            return MultinomialNB()
        if self.__model == '':
            return NuSVC()


    def __generate_train_model_common(self, datasets_categories, dumpFile):
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
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        # 使用支持向量机方法训练分类器
        clf = self.__select_model().fit(X_train_tfidf, datasets_train.target)
        joblib.dump(clf, dumpFile)

    def __generate_page_train_model(self):
        datasets_categories = ['target-pages-' + self.__page_keyword, 'non-target-pages-' + self.__page_keyword]
        path = 'models-machine-learning\\' + self.__model + '_' + self.__page_keyword + '_pages.pkl'
        self.__generate_train_model_common(datasets_categories, path)

    def __generate_line_train_model(self):
        datasets_categories = ['target-lines-' + self.__line_keyword, 'non-target-lines-' + self.__line_keyword]
        path = 'models-machine-learning\\' + self.__model + '_' + self.__line_keyword + '_lines.pkl'
        # self.__generate_train_model_common(datasets_categories, path, WordOnlyTokenizer())
        self.__generate_train_model_common(datasets_categories, path)

    def __generate_paragraph_train_model(self):
        datasets_categories = ['target-paragraphs-' + self.__paragraph_keyword, 'non-target-paragraphs-' + self.__paragraph_keyword]
        path = 'models-machine-learning\\' + self.__model + '_' + self.__paragraph_keyword + '_paragraphs.pkl'
        # self.__generate_train_model_common(datasets_categories, path, WordOnlyTokenizer())
        self.__generate_train_model_common(datasets_categories, path)

    def __validate_model(self):
        n_folds = 10
        seed = 6
        kfold = KFold(n_splits=n_folds, shuffle=True, random_state=seed)
        cv_results = cross_val_score(Pipeline([
            ("Scaler", StandardScaler(with_mean=False)),
            ("Linear_SVC", LinearSVC())
        ]), self._line_tfidf_result, self._datasets_train_line.target, cv=kfold)
        msg = "%s: %f (+/- %f)" % ('Linear_SVC', cv_results.mean(), cv_results.std())
        print(msg)

    def train(self):
        if self.__page_keyword != '':
            self.__generate_page_train_model()
        if self.__line_keyword != '':
            self.__generate_line_train_model()
        if self.__paragraph_keyword != '':
            self.__generate_paragraph_train_model()
        # Uncomment this line to validate the model.
        # self.__validate_model()

# Uncomment these lines to test this class.
# tm = TrainingModel('Income Statements', 'Total Revenue')
# tm.train()
# tm = TrainingModel('Balance Sheets', 'Total Assets')
# tm.train()
# import jieba
# tm = TrainingModel(paragraph_keyword='Law Verdict', encoding='utf-8', binary=True, tokenizer=jieba.cut, model='multinomial_nb')
# tm.train()
