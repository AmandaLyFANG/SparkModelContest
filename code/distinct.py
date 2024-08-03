import json
from collections import defaultdict

# Load the JSON data
with open('../xfdata/train.json', 'r', encoding='utf-8') as file:
# with open('D:\\Individual Resume\\SparkModelContest\\prediction_result\\merged_final_output_test_lq.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


# Initialize a dictionary to store distinct values for each column
distinct_values = defaultdict(set)
distinct_values_count = defaultdict(int)

# Iterate through the records
for recordData in data:
    for record in recordData['infos']:
        for key, value in record.items():
            if isinstance(value, list):
                for item in value:
                    distinct_values[key].add(item)
                    distinct_values_count[key] += len(value)
            else:
                distinct_values[key].add(value)
                if value and value != '':
                    distinct_values_count[key] += 1

# Print the distinct values for each column
for key, values in distinct_values.items():
    print(f"Distinct values for '{key}': {values}")
    print(key, distinct_values_count[key])
print()
print("=================================")
print()
for key, values in distinct_values.items():
    print(key, distinct_values_count[key])

with open('train_sum.txt', 'w', encoding='utf-8') as file:
    file.write(str(distinct_values_count))
    file.write("=============================================")
    file.write(str(distinct_values))
