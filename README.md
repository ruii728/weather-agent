My first AI Agent project.
# Weather Agent

一个基于 DeepSeek + OpenWeather API 的智能天气查询 Agent。

## 功能

- 普通聊天
- 查询实时天气
- 自动识别天气问题
- 自动提取城市名称
- 生成自然语言天气播报

## 技术栈

- Python
- DeepSeek API
- OpenWeather API
- Requests
- python-dotenv

## 项目架构

用户输入

↓

Agent决策

↓

天气查询工具

↓

获取天气数据

↓

LLM生成天气播报

↓

返回结果

## 安装

创建虚拟环境：

```bash
python -m venv .venv
```

激活：

```bash
.venv\Scripts\activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

## 配置环境变量

创建 `.env`

```env
DEEPSEEK_API_KEY=你的DeepSeekKey
OPENWEATHER_API_KEY=你的OpenWeatherKey
```

## 运行

```bash
python app.py
```

## 示例

用户：

```text
帮我查询一下天津天气
```

Agent：

```text
天津目前中雨，气温24.6℃
```