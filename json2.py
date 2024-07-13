import json

# 定义要加载的JSON文件路径
input_file_path = "dataset/train.json"
# 定义要保存的JSONL文件路径
output_file_path = "dataset/train2.json"

# 打开输入文件读取数据
with open(input_file_path, "r", encoding="utf-8") as infile:
    # 读取JSON数据
    data = json.load(infile)

# 检查data是否是一个列表，假设你的JSON文件是一个数组格式
if isinstance(data, list):
    # 打开输出文件准备写入
    with open(output_file_path, "w", encoding="utf-8") as outfile:
        output = []
        # 遍历列表中的每个元素
        for item in data:
            wItem = {}
            wItem["chat_lines"] = item["chat_text"].split("\n")
            # 去除""元素
            wItem["chat_lines"] = [line for line in wItem["chat_lines"] if line]
            
            output.append(wItem)
        outfile.write(json.dumps(output, ensure_ascii=False))
else:
    raise ValueError("JSON文件的内容不是一个列表")

print("JSON ---> JSONL:", output_file_path)
