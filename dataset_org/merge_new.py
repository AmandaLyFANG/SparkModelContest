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
                elif key == "客户是否有卡点" and value == "有卡点":
                    main_body[key] = "有卡点"
                elif key == "客户是否有意向" and value == "有意向":
                    main_body[key] = "有意向"

    return main_body

def merge_records(data):
    result = []

    for index, record in enumerate(data):
        infos_by_name = {}
        first_valid_record = None

        for info in record['infos']:
            name = info['基本信息-姓名']
            if len(name) > 4 or (len(name) > 2 and not name[2:3].isdigit()):
                continue

            # Store the first valid record only
            if not first_valid_record:
                first_valid_record = info
                infos_by_name[name] = info

        # If there's a valid record, process it
        if first_valid_record:
            similar_infos = [first_valid_record] + [other_info for other_info in record['infos'] if other_info['基本信息-姓名'] == first_valid_record['基本信息-姓名']]
            merged_info = (
                merge_info_dicts(similar_infos))
            result.append({"index": index + 1, "infos": [merged_info]})

    return result



# Load JSON data from file
with open('final_retry_long03_修改index08.json', 'r', encoding='utf-8') as f:  # No change
    data = json.load(f)

# Merge the records
merged_data = merge_records(data)

# Save merged data back to JSON file
with open('merged_final_output_test.json', 'w', encoding='utf-8') as f:  # No change
    json.dump(merged_data, f, ensure_ascii=False, indent=4)
