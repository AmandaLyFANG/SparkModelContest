竞赛名：基于星火大模型的群聊对话分角色要素提取挑战赛
参赛队伍：富豪榜前三

1.解决方案及算法介绍文件,模型训练复现流程
整体解决方案：模型的输入为55个对话片段，需要输出对话分角色要素提取的结果，我们团队采用的方案是微调后的星火大模型。
模型微调阶段：团队尝试了原始的Spark Max模型输出结果不理想，所以采用lora微调方式基于spark pro模型进行微调。团队先后进行了2个版本的微调模型，
                         由于大模型的微调的训练集token限制为8000，所以我们版本V1.0微调模型只使用了小于8000的训练集；版本V2.0我们对于大于8000的训练集
                         进行切分，拆分成多段，使用了全部的训练集。这2个版本的微调模型我们后续都在使用，V1.0是我们提取主体信息的模型，V2.0模板是我们用来
                         提取补充信息的模型。之后将这2个模型输出结果合并。本次训练微调采用的讯飞大模型训练平台。微调的参数学习率为0.00008，训练次数为2，
                         训练数据集可查看在线数据集。
模型调用阶段：首先调用V1.0版本微调模型，得到输出结果STEP01；
                         然后基于这个结果按照用户信息合并成单条数据，得到STEP02的结果；
                         之后调用V2.0版本微调模型获取手机号、用户购买阶段等信息，进行合并，分别得到STEP03、STEP04的结果；
                         之后利用程序处理意向产品的数据，然后合并，得到STEP05的结果；
                         最后将STEP05的结果转产csv文件，得到最终结果。
提示词：模型调用阶段均采用统一的提示词用以约定模型的数据格式，提示词保存路径为code/system_03.md 文件。
                       
                   
2.系统依赖(操作系统版本，Python/Matlab的版本)
##这个命令会生成一个requirements.txt文件，其中列出所有的依赖包及其版本。
pip freeze > requirements.txt
## 需要按照的包
# pip install --upgrade spark_ai_python
# pip install sparkai
# pip install requests
python执行涉及到的包如下：
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import json
import re
import csv

3.主要数据处理，执行code/test.sh
其中执行顺序如下：

1    "../code/sft01_longchat_v1.py",
处理目标：用微调V1.0版本模型提取目标主体信息
输入文件："../xfdata/test_data.json"
        "../code/system_03.md"
输出文件："../user_data/try_test_data_v1.json"

2    "../code/merge_name.py",
处理目标：将同一index下姓名相同的信息合并
输入文件：'../user_data/try_test_data_v1.json'
输出文件：'../user_data/merged_final_outputV1.json'

3    "../code/sft01_longchat_v3",
处理目标：用微调V2.0版本模型提取电话号码和购买阶段信息
输入文件："../xfdata/test_data.json"
        "../code/test/system_03.md"
输出文件："../user_data/merged_final_outputV2.json"

4    "../code/merge_phone_number.py",
处理目标：将同一index下姓名相同的电话号码合并
输入文件：'../user_data/merged_final_outputV2.json'
        '../user_data/merged_final_outputV1.json'
输出文件：'../user_data/merged_final_outputV3.json'

5    "../code/merge_purchase_stage.py"

处理目标：将同一index下购买阶段相同的电话号码合并
输入文件：'../user_data/merged_final_outputV2.json'
'../user_data/merged_final_outputV3.json'
输出文件：'../user_data/merged_final_outputV4.json'

6    "../code/merged_intended_product.py"
输入文件：'../xfdata/test_data.json'
        '../user_data/merged_final_outputV4.json'
输出文件：'../user_data/merged_final_outputV5.json'

7    "../code/test/json_to_csv.py"
输入文件：'../user_data/merged_final_outputV5.json'
输出文件：'../prediction_result/result.csv'



