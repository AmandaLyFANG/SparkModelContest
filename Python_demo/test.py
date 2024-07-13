import SparkApi

# 以下密钥信息从控制台获取
appid = "5d1dff54"  # 填写控制台中获取的 APPID 信息
api_secret = "YjFjZTAwOTkzZTQxMWU1ZDE5MGY3ODlm"  # 填写控制台中获取的 APISecret 信息
api_key = "7a18122f8fe839bf86a32d4030eb0703"  # 填写控制台中获取的 APIKey 信息

# 调用微调大模型时，设置为“patch”
domain = "patchv3"
patch_id = ""

# 云端环境的服务地址
# Spark_url = "wss://spark-api-n.xf-yun.com/v1.1/chat"  # 微调v1.5环境的地址
Spark_url = "wss://spark-api-n.xf-yun.com/v3.1/chat"  # 微调v3.0环境的地址


text = []

# length = 0


def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while getlength(text) > 8000:
        del text[0]
    return text


if __name__ == "__main__":
    text.clear
    while 1:
        Input = input("\n" + "我:")
        question = checklen(getText("user", Input))
        SparkApi.answer = ""
        print("星火:", end="")
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question, patch_id)
        getText("assistant", SparkApi.answer)
        print(str(text[-1]))
