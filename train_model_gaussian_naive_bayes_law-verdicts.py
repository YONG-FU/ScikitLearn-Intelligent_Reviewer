from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
from jieba import cut


datasets_categories = ["target-paragraphs-law-verdicts", "non-target-paragraphs-law-verdicts"]

# 从硬盘获取训练数据
datasets_train = load_files("datasets-train",
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

# 使用高斯朴素贝叶斯方法训练分类器
clf = GaussianNB().fit(X_train_tfidf, datasets_train.target)
model = "models-machine-learning\\gaussian_naive_bayes_law-verdicts_paragraphs.pkl"
joblib.dump(clf, model)