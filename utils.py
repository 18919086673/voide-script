from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# 导入维基百科的包装类
from langchain_community.utilities import WikipediaAPIWrapper
import os

# 通过key从环境变量中读取api_key
openai_api_key = os.getenv("OPENAI_API_KEY")
print("openai_api_key=", openai_api_key)


def generate_script(subject, video_length, creativity, api_key):
    # 1. 定义标题模板
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )
    # 定义脚本模板
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住眼球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```
             {wikipedia_search}
            ```
            """)
        ]
    )
    # 3. 定义OpenAI模型对象
    model = ChatOpenAI(model="gpt-3.5-turbo",
                       openai_api_key=api_key,
                       openai_api_base="https://api.aigc369.com/v1",
                       temperature=creativity)
    # 4. 定义标题链
    title_chain = title_template | model
    # 5. 定义脚本链
    script_chain = script_template | model
    # 6.调用标题模板的invoke方法得到PromptValue类型的对象传递给大模型并解析出大模型响应的内容
    title = title_chain.invoke({"subject": subject}).content
    # 7. 实例化维基百科对象并指定返回结果使用中文
    # 注意：维基百科在国内没法直接访问，需要翻墙，开启安心加速球，否则报错：
    search = WikipediaAPIWrapper(lang="zh")
    # 8. 调用维基百科的run()方法传递标题得到维基百科的搜索结果
    search_relult = search.run(subject)
    print(search_relult)
    # 9.调用脚本链的invoke()方法得到大模型输出的脚步内容
    script = script_chain.invoke({"title": title, "duration": video_length, "wikipedia_search": search_relult}).content
    # 返回结果：维基百科的搜索结果,视频标题，视频脚本内容
    return search_relult, title, script


print(generate_script("光辉岁月", 1, 0.7, os.getenv("OPENAI_API_KEY")))
