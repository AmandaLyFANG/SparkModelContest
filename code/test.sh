/bin/sh "test.sh"

@echo off
echo Running scripts in sequence...

python sft01_longchat_v1.py
python sft01_longchat_v3.py
python merge_name.py
python merge_phone_number.py
python merge_purchase_stage.py
python merge_intended_product.py
python json_to_csv.py

echo All scripts have been executed.
pause