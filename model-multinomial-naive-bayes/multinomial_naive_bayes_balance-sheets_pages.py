from os import listdir, path
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.externals import joblib

# 选取参与分析的文本类别
datasets_categories = ["target-pages-balance-sheets", "non-target-pages-balance-sheets"]

# 从硬盘获取训练数据
datasets_train = load_files("..\\datasets-train",
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
tfidf_transformer.fit_transform(X_train_counts)

# 载入已经训练好的分类器
clf = joblib.load("..\\models-machine-learning\\multinomial_naive_bayes_balance-sheets_pages.pkl")

# 读入需要分析预测的文件
folder_path_annual_reports = path.dirname(path.dirname(path.abspath(__file__))) + "\\documents-convert\\pages-annual-reports"
pages_folder_name_list = listdir(folder_path_annual_reports)

for pages_folder in pages_folder_name_list:
    print(pages_folder)
    pages_text_file_name_list = listdir(folder_path_annual_reports + "\\" + pages_folder)

    for file_name in pages_text_file_name_list:
        with open (folder_path_annual_reports + "\\" + pages_folder + "\\" + file_name, encoding="utf-8") as text_file_object:
            if text_file_object:
                # 预测用的新字符串
                docs_new = [text_file_object.read()]

                # 字符串向量化处理
                X_new_counts = count_vectorizer.transform(docs_new)
                X_new_tfidf = tfidf_transformer.transform(X_new_counts)

                # 进行机器学习预测
                predicted = clf.predict(X_new_tfidf)

                # 打印预测结果
                if datasets_train.target_names[predicted[0]] == "target-pages-balance-sheets":
                    print(file_name + " => " + datasets_train.target_names[predicted[0]])
                    print(predicted[0])