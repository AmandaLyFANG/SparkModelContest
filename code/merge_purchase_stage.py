import json

# 加载 JSON 文件
     ## 用微调模型输出姓名和用户购买阶段的文件file1（只取其中的用户购买阶段）
     ## merge 姓名的主题文件为file2
with open('../user_data/merged_final_outputV2.json', 'r', encoding='utf-8') as file1, \
     open('../user_data/merged_final_outputV3.json', 'r', encoding='utf-8') as file2:
    data1 = json.load(file1)
    data2 = json.load(file2)

# 创建从 (index, name) 到用户购买阶段的映射
stage_mapping = {}

for entry1 in data1:
    index = entry1.get('index')
    for info1 in entry1["infos"]:
        name = info1.get('基本信息-姓名')
        phone = info1.get('客户购买阶段')
        if index and name and phone:
            stage_mapping[(index, name)] = phone

# 使用映射填充 data2 中的手机号码
for entry2 in data2:
    index = entry2.get('index')
    infos = entry2.get('infos', [])
    for info2 in infos:
        name = info2.get('基本信息-姓名')
        if (index, name) in stage_mapping:
            info2['客户购买阶段'] = stage_mapping[(index, name)]

# 输出合并后的结果到文件 ## merge 电话号码后最终的输出文件
with open('../user_data/merged_final_outputV4.json', 'w', encoding='utf-8') as output_file:
    json.dump(data2, output_file, ensure_ascii=False, indent=4)


