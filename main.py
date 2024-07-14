from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

import json
import re

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


def chat(userContent, chatHistory=None):
    if chatHistory is None:
        chatHistory = newHistory()
    chatHistory.append(buildMessage(userContent, role="user"))
    handler = ChunkPrintHandler()
    assistantContent = (
        spark.generate([chatHistory], callbacks=[handler]).generations[0][0].text
    )
    chatHistory.append(buildMessage(assistantContent, role="assistant"))
    return assistantContent, chatHistory


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
    return assistantContent, history


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
    prompt = """角色设定：你是一个商务群聊记录分析师，可以从给定的<客服>与<客户>的群聊对话中, 提取出指定的字段信息。
思考建议：
1.首先，对每条聊天记录进行分词处理，以便后续提取关键词。
2.然后，根据关键词匹配规则，提取出咨询类型、意向产品、购买异议点和下一步跟进计划-参与人等字段。
3.对于其他字段，如基本信息、客户预算、竞品信息、客户是否有意向、客户是否有卡点、客户购买阶段以及下一步跟进计划的详细事项，可以根据关键词匹配规则，提取出相应的内容。
4.如果对话中未提及某个字段的信息，可以将该字段的值设为空字符串。
5.最后，将提取出的字段信息按照给定的JSON格式输出。
字段说明：咨询类型、意向产品、购买异议点、下一步跟进计划-参与人，4个字段的类型是字符串数组，可能有多条内容["aaa","bbb"]，也可能没有内容[]。其余字段都是字符串类型，如果为空请填写""。
客户是否有卡点可以从这些选项中考虑：有卡点 和 无卡点。客户是否有意向可以从这些选项中考虑：有意向 或 无意向。
咨询类型可以从这些选项中考虑：询价、答疑、吐槽。
意向产品可以从这些选项中考虑：高级版、标准版、定制版、会话存档、CRM、商城、开放接口、运营服务。
购买异议点可以从这些选项中考虑：产品功能、价格、竞品、客户内部问题。
根据思考建议对输入聊天内容进行分析，将分析得到的结果填入返回值模板中对应的条目，在进行结果填写时，不允许修改返回值模板中的内容。
请将提取的信息输出成一个JSON对象，所有字段均为String类型，其中："咨询类型"、"意向产品"、"购买异议点"、"下一步跟进计划-参与人"，这四个字段为字符串类型的列表。
输出必须严格遵循表单格式的字段及顺序，字段名必须按照表单格式输出，在对话中未找到相关信息的字段留空，不能删除字段，直接输出JSON。"""

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
            if len(prompt) + len(item["chat_text"]) < 8192:
                resp, history = chat(
                    userContent=item["chat_text"], history=newHistory(prompt)
                )

            else:
                resp, history = longChat(
                    userContent=item["chat_text"], history=newHistory(prompt)
                )
            resp = re.sub(r'^```json\n|```$', '', resp, flags=re.MULTILINE)
            print(resp)

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
