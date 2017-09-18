from time import strftime, localtime

class GenerationDataset:
    # 定义基本属性
    feedback_json = []

    # 定义构造方法
    def __init__(self, feedback_json):
        self.feedback_json = feedback_json

    def generateData(self):
        feedback_keywords = self.feedback_json["keywords"]
        for feedback_keyword in feedback_keywords:
            for feedback in feedback_keyword["values"]:
                if "feedback" in feedback:
                    if feedback["feedback"]["type"] == "pages" and feedback_keyword["keyword"] == "Total Assets":
                        keyword_value = "balance-sheets"
                    elif feedback["feedback"]["type"] == "pages" and feedback_keyword["keyword"] == "Total Revenue":
                        keyword_value = "income-statements"
                    else:
                        keyword_value = feedback_keyword["keyword"].lower().replace(' ', '-')

                    datasets_directory_name = "datasets-train\\" + feedback["feedback"]["result"] + "-" + feedback["feedback"]["type"] + "-" + keyword_value + "\\"
                    file_name = self.feedback_json["name"] +\
                                "[Page " + str(feedback["page"]) +\
                                " Line " + str(feedback["line"]) + "] " +\
                                strftime("%Y-%m-%d-%H-%M-%S", localtime()) + ".txt"
                    with open(datasets_directory_name + file_name, "w", encoding="utf-8") as retrained_data_file_object:
                        retrained_data_file_object.write(feedback["textToHighlight"])