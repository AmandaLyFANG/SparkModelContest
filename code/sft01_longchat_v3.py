from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

import json
import re

# 星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = "wss://spark-api-n.xf-yun.com/v3.1/chat"
# SPARKAI_URL = "wss://spark-api-n.xf-yun.com/v3.1/chat"
# 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = "e9d98357"
SPARKAI_API_SECRET = "M2YwNGU2ZjkzOWJmNDA4ZDU0MGEzMzc4"
SPARKAI_API_KEY = "f1647a1dd5ff62881f44f55c0d2b23cf"
# 星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = "patchv3"

spark = ChatSparkLLM(
    spark_api_url=SPARKAI_URL,
    spark_app_id=SPARKAI_APP_ID,
    spark_api_key=SPARKAI_API_KEY,
    spark_api_secret=SPARKAI_API_SECRET,
    spark_llm_domain=SPARKAI_DOMAIN,
    streaming=False,
    top_k=1,
    max_tokens=8192,
    request_timeout=180,
)
spark.temperature = 0.1


def newHistory(systemContent=None):
    if systemContent is None:
        return []
    return [buildMessage(systemContent, role="system")]


def buildMessage(content, role="user"):
    return ChatMessage(content=content, role=role)


def chat(userContent, history=None):
    if history is None:
        history = newHistory()
    history.append(buildMessage(userContent, role="user"))
    handler = ChunkPrintHandler()
    assistantContent = (
        spark.generate([history], callbacks=[handler]).generations[0][0].text
    )
    history.append(buildMessage(assistantContent, role="assistant"))
    return (assistantContent, history)


if __name__ == "__main__":
    # 从文件中读取内容
    try:
        with open("system_03.md", "r", encoding="utf-8") as f:
            systemContent = f.read()
    except FileNotFoundError:
        print("系统文件未找到")
        exit()

    # 从json文件中读取内容
    try:
        with open("../xfdata/test_data.json", "r", encoding="utf-8") as f:
            trainData = json.load(f)
    except FileNotFoundError:
        print("数据文件未找到")
        exit()

    final = []
    index = 1
    for item in trainData:
        answer = {"index": index}
        print("index: ", index)
        print("request len: ", len(systemContent) + len(item["chat_text"]))
        answer["infos"] = []
        try:
            if len(systemContent) + len(item["chat_text"]) < 8192:
                resp, history = chat(
                    userContent=item["chat_text"], history=newHistory(systemContent)
                )
                # 使用正则表达式去除前缀和后缀
                cleaned_resp = re.sub(r'^```json\n|```$', '', resp, flags=re.MULTILINE)
                # 将单引号替换成双引号
                cleaned_resp = cleaned_resp.replace("'", '"')
                answer["infos"] = json.loads(cleaned_resp)
            else:
                # 对于长文本分块处理，最后进行merge
                userContentBlocks = []
                for i in range(0, len(item["chat_text"]), 7100):
                    if i + 7100 > len(item["chat_text"]):
                        userContentBlocks.append(item["chat_text"][i:])

                    elif i == 0:
                        userContentBlocks.append(item["chat_text"][i: i + 7100])
                    else:
                        userContentBlocks.append(item["chat_text"][i - 600: i + 7100])
                # 切分块完成之后，循环调用大模型
                for block in userContentBlocks:
                    # print("userContentBlocks:",block)

                    resp, history = chat(userContent=block, history=newHistory(systemContent))
                    # 使用正则表达式去除前缀和后缀
                    cleaned_resp = re.sub(r'^```json\n|```$', '', resp, flags=re.MULTILINE)
                    # 将单引号替换成双引号
                    cleaned_resp = cleaned_resp.replace("'", '"')
                    # print("resp_xunhuan:",cleaned_resp)
                    # 转json格式后提取字典第一个元素，然后循环累加到list中，得到最终的list列表，每个元素是结果字典的形式
                    answer["infos"].append(json.loads(cleaned_resp)[0])
                    # answer["infos"] = [json.loads(cleaned_resp)[0]] + answer["infos"]
        except Exception as e:  # 可以根据需要修改异常类型
            print(f"处理过程中出现错误: {e}")
            answer["infos"] = []
        index += 1
        final.append(answer)

    # 写入JSON文件，确保非ASCII字符正确写入
    try:
        with open("../user_data/merged_final_outputV2.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(final, indent=4, ensure_ascii=False))
    except IOError:
        print("写入文件时发生错误")
