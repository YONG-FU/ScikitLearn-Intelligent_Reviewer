from os import listdir, path, makedirs
from re import findall

folder_path = "..\\datasets-train\\target-pages-income-statements"
target_pages_income_statements_name_list = listdir(folder_path)

for file_name in target_pages_income_statements_name_list:
    print(file_name)

    with open(folder_path + "\\" + file_name, encoding="utf8") as page_text_file_object:
        lines_text_folder_name = "lines-total-revenues\\" + file_name[:-4]

        if not path.exists(lines_text_folder_name):
            makedirs(lines_text_folder_name)

        line_index = 1
        for line_text in page_text_file_object.readlines():
            total_revenue_pattern = "TOTAL|Total|total|REVENUE|Revenue|revenue|NET SALES|Net Sales|Net sales|Netsales|net sales|netsales"
            total_revenue_pattern_result = findall(total_revenue_pattern, line_text)

            # letter_pattern = "[A-Za-z]"
            # letter_pattern_result = findall(letter_pattern, line_text)
            number_pattern = "[0-9]"
            number_pattern_result = findall(number_pattern, line_text)

            if len(total_revenue_pattern_result) > 0 and len(number_pattern_result) > 0:
                with open(lines_text_folder_name + "\\" + file_name[:-5] + " Line " + str(line_index) + "].txt", "w", encoding='utf-8') as text_file_object:
                    text_file_object.write(line_text)

            line_index = line_index + 1