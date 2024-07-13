import json

# 定义要加载的JSON文件路径
input_file_path = "dataset/train.json"
# 定义要保存的JSONL文件路径
output_file_path = "dataset/train_len_limited.jsonl"

# 打开输入文件读取数据
with open(input_file_path, "r", encoding="utf-8") as infile:
    # 读取JSON数据
    data = json.load(infile)

# 检查data是否是一个列表，假设你的JSON文件是一个数组格式
if isinstance(data, list):
    # 打开输出文件准备写入
    with open(output_file_path, "w", encoding="utf-8") as outfile:
        # 遍历列表中的每个元素
        for item in data:
            if len(item["chat_text"]) + len(str(item["infos"])) <= 8000:
                wItem = {}
                wItem["input"] = item["chat_text"]
                wItem["target"] = str(item["infos"])
                # 将每个元素转换为JSON字符串并写入到文件，每个元素占一行
                outfile.write(json.dumps(wItem, ensure_ascii=False) + "\n")
else:
    raise ValueError("JSON文件的内容不是一个列表")

print("JSON ---> JSONL:", output_file_path)
