import json
import csv

# 读取JSON文件
with open('../user_data/merged_final_outputV5.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 提取数据
data_list = []
for item in data:
    data_list.extend(item["infos"])

# 获取CSV列名
columns = data_list[0].keys()

# 写入CSV文件
with open('../prediction_result/result.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(data_list)

print("JSON文件已成功转换为CSV文件。")
