from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

import json

# 星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = "wss://spark-api.xf-yun.com/v3.5/chat"
# SPARKAI_URL = "wss://spark-api-n.xf-yun.com/v3.1/chat"
# 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = "5d1dff54"
SPARKAI_API_SECRET = "YjFjZTAwOTkzZTQxMWU1ZDE5MGY3ODlm"
SPARKAI_API_KEY = "7a18122f8fe839bf86a32d4030eb0703"
# appid = "5d1dff54"  # 填写控制台中获取的 APPID 信息
# api_secret = "YjFjZTAwOTkzZTQxMWU1ZDE5MGY3ODlm"  # 填写控制台中获取的 APISecret 信息
# api_key = "7a18122f8fe839bf86a32d4030eb0703"  # 填写控制台中获取的 APIKey 信息
# 星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = "generalv3.5"

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


# for context over 8192 max_tokens, divided into multi-blocks
def longChat(userContent, history=None):
    if history is None:
        history = newHistory()
    userContentBlocks = []
    for i in range(0, len(userContent), 6600):
        if i + 6600 > len(userContent):
            userContentBlocks.append(userContent[i:])
        elif i == 0:
            userContentBlocks.append(userContent[i : i + 6600])
        else:
            userContentBlocks.append(userContent[i - 600 : i + 6600])
    lastResult = None
    for block in userContentBlocks:
        if lastResult is not None:
            history.append(
                buildMessage(
                    block + f"\n可参考的历史对话分析结果：{lastResult}",
                    role="user",
                )
            )
        else:
            history.append(buildMessage(block, role="user"))
        handler = ChunkPrintHandler()
        assistantContent = (
            spark.generate([history], callbacks=[handler]).generations[0][0].text
        )
        # print("history: ", history)
        # print("assistant: ", assistantContent)
        if lastResult is not None:
            lastResult = mergeInfos(lastResult, assistantContent)
        else:
            lastResult = assistantContent
        history.pop()

    history.append(buildMessage(assistantContent, role="assistant"))
    return (assistantContent, history)


with open("merge.md", "r", encoding="utf-8") as f:
    mergeContent = f.read()


def mergeInfos(last, current):
    resp, history = chat(
        userContent=f"历史分析结果：{last}\n当前分析结果：{current}",
        history=newHistory(mergeContent),
    )
    return resp


if __name__ == "__main__":
    # 从文件中读取内容
    try:
        with open("system.md", "r", encoding="utf-8") as f:
            systemContent = f.read()
    except FileNotFoundError:
        print("系统文件未找到")
        exit()

    # 从json文件中读取内容
    try:
        with open("dataset/train.json", "r", encoding="utf-8") as f:
            trainData = json.load(f)
    except FileNotFoundError:
        print("数据文件未找到")
        exit()
    print(len(trainData))

    final = []
    index = 1
    for item in trainData[0:5]:
        answer = {"index": index}
        print("index: ", index)
        print("request len: ", len(systemContent) + len(item["chat_text"]))
        try:
            if len(systemContent) + len(item["chat_text"]) < 8192:
                resp, history = chat(
                    userContent=item["chat_text"], history=newHistory(systemContent)
                )
                answer["infos"] = json.loads(resp)
            else:
                resp, history = longChat(
                    userContent=item["chat_text"], history=newHistory(systemContent)
                )
                answer["infos"] = json.loads(resp)
        except Exception as e:  # 可以根据需要修改异常类型
            print(f"处理过程中出现错误: {e}")
            answer["infos"] = []
        index += 1
        final.append(answer)

    # 写入JSON文件，确保非ASCII字符正确写入
    try:
        with open("final_retry.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(final, ensure_ascii=False))
    except IOError:
        print("写入文件时发生错误")
