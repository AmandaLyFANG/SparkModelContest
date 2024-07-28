import json

with open('D:\\Individual Resume\\SparkModelContest\\dataset_org\\test_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for i in range(len(data)):
    data[i]["index"] = i+1

    with open('test-data/text'+str(data[i]["index"])+'_'+str(str(len(data[i]["chat_text"])))+'.txt', "w", encoding="utf-8") as f:
        f.write(data[i]["chat_text"])
