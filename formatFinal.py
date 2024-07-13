import json

# 加载基准JSON文件
with open("stdItem.json", "r", encoding="utf-8") as file:
    base_data = json.load(file)

# 加载需要比对的JSON文件
with open("final.json", "r", encoding="utf-8") as file:
    compare_data = json.load(file)

listColumns = ["咨询类型", "意向产品", "购买异议点", "下一步跟进计划-参与人"]


# 检查字段是否合规
def check_compliance(base, compare):
    print("开始比对...\n\n", base, compare)
    for key, value in base.items():
        if key not in compare:
            print(f"字段 '{key}' 在 'compare.json' 中缺失。")
        elif not isinstance(compare[key], type(value)):
            print(
                f"字段 '{key}' 类型不匹配，'base.json' 中为 {type(value).__name__}, 'compare.json' 中为 {type(compare[key]).__name__}。"
            )
            if type(value) == str and type(compare[key]) == list:
                if len(compare[key]) > 0:
                    compare[key] = compare[key][0]
                else:
                    compare[key] = ""
            elif type(value) == list and type(compare[key]) == str:
                compare[key] = [compare[key]]
        else:
            # 这里可以添加更多的比对逻辑，例如值的比较等
            print(f"字段 '{key}' 比对通过。")
    print("\n\n")


for line in compare_data:
    for info in line["infos"]:
        check_compliance(base_data, info)

with open("finalFormat.json", "w", encoding="utf-8") as file:
    json.dump(compare_data, file, ensure_ascii=False)
