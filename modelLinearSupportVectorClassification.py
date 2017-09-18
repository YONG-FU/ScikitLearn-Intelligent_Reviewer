from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

class TrainingModel:
    def __init__(self, page_keyword, line_keyword):
        self.__page_keyword = page_keyword.lower().replace(' ', '-')
        self.__line_keyword = line_keyword.lower().replace(' ', '-')

    def __generate_train_model_common(self, datasets_categories, dumpFile):
        # 从硬盘获取训练数据
        datasets_train = load_files("datasets-train",
                                    categories=datasets_categories,
                                    load_content=True,
                                    encoding="utf-8",
                                    decode_error="strict",
                                    shuffle=True)

        # 统计词语出现次数
        count_vectorizer = CountVectorizer()
        X_train_counts = count_vectorizer.fit_transform(datasets_train.data)

        # 使用tf-idf方法提取文本特征
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        # 使用支持向量机方法训练分类器
        clf = LinearSVC().fit(X_train_tfidf, datasets_train.target)
        joblib.dump(clf, dumpFile)

    def __generate_page_train_model(self):
        datasets_categories = ['target-pages-' + self.__page_keyword, 'non-target-pages-' + self.__page_keyword]
        path = 'models-machine-learning\\linear_support_vector_classification_' + self.__page_keyword + '_pages.pkl'
        self.__generate_train_model_common(datasets_categories, path)

    def __generate_line_train_model(self):
        datasets_categories = ['target-lines-' + self.__line_keyword, 'non-target-lines-' + self.__line_keyword]
        path = 'models-machine-learning\\linear_support_vector_classification_' + self.__line_keyword + '_lines.pkl'
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
        self.__generate_page_train_model()
        self.__generate_line_train_model()
        # Uncomment this line to validate the model.
        # self.__validate_model()

# Uncomment these lines to test this class.
# tm = TrainingModel('Income Statements', 'Total Revenues')
# tm.train()
# tm = TrainingModel('Balance Sheets', 'Total Assets')
# tm.train()