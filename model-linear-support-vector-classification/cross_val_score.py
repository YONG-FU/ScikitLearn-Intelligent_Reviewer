from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score

from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression, Ridge, Lasso
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import ExtraTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.dummy import DummyClassifier
from sklearn.neural_network import MLPClassifier

seed = 7
pipelines = []

pipelines.append(
                ("NB",
                 Pipeline([
                  ("Scaler", StandardScaler(with_mean=False)),
                  ("NaiveBayes", MultinomialNB())
                 ]))
                )

pipelines.append(
                ("Ridge",
                 Pipeline([
                     ("Scaler", StandardScaler(with_mean=False)),
                     ("Ridge", Ridge(random_state=seed))
                      ]))
                )

pipelines.append(
                ("Lasso",
                 Pipeline([
                     ("Scaler", StandardScaler(with_mean=False)),
                     ("Lasso", Lasso(random_state=seed))
                      ]))
                )

pipelines.append(
                ("Kernel_SVC",
                 Pipeline([
                     ("Scaler", StandardScaler(with_mean=False)),
                     ("SVC", SVC(kernel = 'poly', degree = 3))
                 ])
                )
                )

pipelines.append(
                ("Linear_SVC",
                 Pipeline([
                     ("Scaler", StandardScaler(with_mean=False)),
                     ("Linear_SVC", LinearSVC())
                 ])
                )
                )

pipelines.append(
                ("RF",
                 Pipeline([
                     ("Scaler", StandardScaler(with_mean=False)),
                     ("RF", RandomForestClassifier(random_state=seed))
                 ])
                )
                )

pipelines.append(
                ("ET",
                 Pipeline([
                     ("Scaler", StandardScaler(with_mean=False)),
                     ("ET", ExtraTreeClassifier(random_state=seed))
                 ])
                )
                )

pipelines.append(
                ("BR",
                 Pipeline([
                     ("Scaler", StandardScaler(with_mean=False)),
                     ("BR", BaggingClassifier(random_state=seed))
                 ])
                )
                )

pipelines.append(
                ("Dummy",
                 Pipeline([
                     ("Dummy", DummyClassifier(strategy = 'most_frequent'))
                 ])
                )
                )

pipelines.append(
                ("Neural Network",
                 Pipeline([
                     ("Neural Network", MLPClassifier(alpha=1))
                 ])
                )
                )


from os import listdir, path
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.externals import joblib
from jieba import cut

# 选取参与分析的文本类别
datasets_categories = ["target-paragraphs-law-verdicts", "non-target-paragraphs-law-verdicts"]

# 从硬盘获取训练数据
datasets_train = load_files("..\\datasets-train",
                            categories=datasets_categories,
                            load_content=True,
                            encoding="utf-8",
                            decode_error="strict",
                            shuffle=True)

# 统计词语出现次数
count_vectorizer = CountVectorizer(binary=True, tokenizer=cut)
X_train_counts = count_vectorizer.fit_transform(datasets_train.data)

# 使用tf-idf方法提取文本特征
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# 载入已经训练好的分类器
clf = joblib.load("..\\models-machine-learning\\linear_support_vector_classification_law-verdicts_paragraphs.pkl")

# 读入需要分析预测的文件
folder_path_lines = path.dirname(path.dirname(path.abspath(__file__))) + "\\documents-convert\\paragraphs-law-verdicts"
paragraphs_folder_name_list = listdir(folder_path_lines)


scoring = 'f1'
n_folds = 10


for name, model in pipelines:
    kfold = KFold(n_splits=n_folds, shuffle=True, random_state=seed)
    cv_results = cross_val_score(model, X_train_tfidf, datasets_train.target, cv=kfold)
    msg = "%s: %f (+/- %f)" % (name, cv_results.mean(),  cv_results.std())
    print(msg)
    print(cv_results)

print(datasets_train.target)