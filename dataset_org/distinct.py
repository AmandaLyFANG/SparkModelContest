import json
from collections import defaultdict

# Load the JSON data
with open('D:\\Individual Resume\\SparkModelContest\\dataset\\train.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize a dictionary to store distinct values for each column
distinct_values = defaultdict(set)

# Iterate through the records
for recordData in data:
    for record in recordData['infos']:
        for key, value in record.items():
            if isinstance(value, list):
                for item in value:
                    distinct_values[key].add(item)
            else:
                distinct_values[key].add(value)

# Print the distinct values for each column
for key, values in distinct_values.items():
    print(f"Distinct values for '{key}': {values}")
