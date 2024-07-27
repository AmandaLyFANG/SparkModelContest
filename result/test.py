import json

with open('D:\\Individual Resume\\SparkModelContest\\dataset_org\\test_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for i in range(len(data)):
    data[i]["index"] = i+1

with open('test_index.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)