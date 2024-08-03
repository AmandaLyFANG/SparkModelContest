import json

product_list = ['会话存档', '标准版', '定制版', '商城', '高级版', '运营服务', '开放接口', 'CRM', '外呼']


def find_products_in_list(chattext, product_list):
    found_products = []
    for product in product_list:
        # 删去对话模板带来的影响
        if product == 'CRM' and 'SCRM' in chattext:
            continue
        if product in chattext:
            found_products.append(product)
    return found_products


def preprocess(chatcontent):
    resultstr = item['chat_text'].replace('本应用会话存档功能将于近期进行升级，升级后不再存档未开通使用权限的员工会话。', '')
    resultstr = resultstr.replace('巨石蓝海SCRM', '')
    resultstr = resultstr.replace('巨石蓝海CRM', '')
    resultstr = resultstr.replace('接下来的运营服务由', '')
    resultstr = resultstr.replace('无商城', '')
    resultstr = resultstr.replace('不含商城', '')
    resultstr = resultstr.replace('本周重点播报已更新，涉及商城装修改造！', '')
    return resultstr


# 读取 test_data.json 并处理
with open('../xfdata/test_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

results = []
index = 1
for item in data:
    item['index'] = index
    item['chat_text'] = preprocess(item['chat_text'])
    result = find_products_in_list(item['chat_text'], product_list)
    results.append((index, result))
    index += 1

# 读取 merged_final_outputV4.json
with open('../user_data/merged_final_outputV4.json', 'r', encoding='utf-8') as file:
    merged_data = json.load(file)

# 将结果合并到 merged_final_outputV4.json 的 "意向产品" 字段中
for res in results:
    index, found_products = res
    for entry in merged_data:
        if entry['index'] == index:
            for info in entry['infos']:
                product_set = set(found_products + info['意向产品'])
                info['意向产品'] = list(product_set)

# 将更新后的数据写回 merged_final_outputV4.json
with open('../user_data/merged_final_outputV5.json', 'w', encoding='utf-8') as file:
    json.dump(merged_data, file, ensure_ascii=False, indent=4)

print("更新完成")
