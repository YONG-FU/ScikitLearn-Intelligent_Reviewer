from os import listdir, stat
from pymongo import MongoClient

# Local Connection Database
# client = MongoClient()

# Cloud Connection Database
uri = "report-reader.southeastasia.cloudapp.azure.com:27017"
client = MongoClient(uri)

database = client["report-reader-database"]
collection = database["verdicts"]
collection.remove()
folder_name = "static\\documents\\docx-law-verdicts-test\\"
docx_file_name_list = listdir(folder_name)

for file_name in docx_file_name_list:
    file_info = stat(folder_name + file_name)
    file_size_bytes = file_info.st_size
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if file_size_bytes < 1024.0:
            file_size_format = "%3.1f %s" % (file_size_bytes, unit)
            break
        file_size_bytes /= 1024.0
    collection.insert_one({"name": file_name[:-5], "size": file_size_format})
    print(file_name[:-4])
    print(file_size_format)