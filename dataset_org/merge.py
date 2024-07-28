# 根据客户名称对内容进行合并，以第一个为主体，保留剩余的内容
# 单值字段：保留有卡点，有意向
# list累加 排重
# 名字超4个字删除，如果名字第三个字符不为数字也删除

import json


def merge_info_dicts(dict_list):
    main_body = dict_list[0]

    for info_dict in dict_list[1:]:
        for key, value in info_dict.items():
            if isinstance(value, list):
                main_body[key] = list(set(main_body[key] + value))
            else:
                if not main_body[key] or main_body[key] == "":
                    main_body[key] = value
                elif key == "客户是否有卡点":
                    if value == "有卡点":
                        main_body[key] = "有卡点"

    return main_body


def merge_records(data):
    for record in data:
        infos = []
        for info in record['infos']:
            info['基本信息-姓名'] = info['基本信息-姓名'][0:3]
            if not info['基本信息-姓名'][2:3].isdigit():
                continue
            infos.append(info)
        record["infos"] = [merge_info_dicts(infos)]

    return data


with open('final_retry_long03_修改index08.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

final_data = merge_records(raw_data)

with open('merge_final_retry_long03_after.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)

# Print the merged data
# print(json.dumps(merged_data, ensure_ascii=False, indent=4))
