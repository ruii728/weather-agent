import os
import requests

from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

messages = [
    {
        "role":"system",
        "content":"你是天气助手"
    }
]

def get_weather(city):
    """
    获取真实天气
    """

    api_key = os.environ.get('OPENWEATHER_API_KEY')

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={api_key}"
        f"&units=metric"
        f"&lang=zh_cn"
    )

    response = requests.get(url)

    data = response.json()

    if data.get("cod") != 200:
        return None

    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"]
    }

def decide_action(user_input):

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role":"system",
                "content":"""
你是Agent决策器。

你有一个工具：

get_weather(city)

如果用户在询问天气：

返回：

WEATHER:城市名

例如：

北京天气
↓

WEATHER:Beijing

帮我查天津天气
↓

WEATHER:Tianjin

上海今天下雨吗
↓

WEATHER:Shanghai

如果不是天气问题：

返回：

CHAT

不要解释。
只返回结果。
"""
            },
            {
                "role":"user",
                "content":user_input
            }
        ]
    )

    return response.choices[0].message.content.strip()

def generate_weather_report(city, weather_data):
    """根据天气数据生成播报"""
    prompt = f"""
请根据以下天气信息生成自然流畅的天气播报：

城市：{city}
天气：{weather_data['weather']}
温度：{weather_data['temp']}
湿度：{weather_data['humidity']}

要求：
1. 使用中文
2. 像天气预报一样自然
3. 不要使用Markdown
"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是一位专业天气播报员。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content

while True:
    user_input = input("请输入：")

    if user_input in ["退出", "exit", "quit"]:
        break

    action = decide_action(user_input)

    print("Agent决策:", action)
    if action.startswith("WEATHER:"):   #AI决定调用天气工具
        city = action.replace("WEATHER:", "").strip()
        weather = get_weather(city)

        if weather is None:
            print("未查询到该城市天气")
            continue
    
   
        report = generate_weather_report(city, weather)
        print("天气播报：", report)

    elif action == "CHAT":
        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )

        ai_reply = response.choices[0].message.content

        print("AI：", ai_reply)

        messages.append(
            {
                "role": "assistant",
                "content": ai_reply
            }
        )
            

        




