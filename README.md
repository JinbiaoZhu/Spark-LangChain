# Spark-LangChain

将 [讯飞星火认知大模型](https://xinghuo.xfyun.cn/) 的 Web 调用接口封装成易用的 python 类，并于 [LangChain](https://github.com/langchain-ai/langchain) 库结合，实现一些复杂的任务。

## Installation

在使用之前，你需要 [申请](https://www.xfyun.cn/solutions/xinghuoAPI) ，以获得 `APPID` 、 `APISecret` 和 `APIKey` 。

```
conda create -n spark python==3.11
```
```
conda activate spark
```
```
git clone https://github.com/JinbiaoZhu/Spark-LangChain.git
```
```
cd spark
```
```
pip install -r requirements.txt
```
在 `.env` 环境中，将申请好的 `APPID` 、 `APISecret` 和 `APIKey` 内容添加进来并保存。

在确保联网的情况下使用！

## File Description

 1. `SparkApiOfficial.py` ：官方API调用示例。
 2. `SparkApiPackaging.py` ：将官方API封装成一个简单的python类 `SparkLLMBase()` 。

    可以实现单次响应，也可以实现聊天式响应（可输出聊天记录到屏幕）。
 3. `SparkApiLangChain.py` ：用 [LangChain](https://github.com/langchain-ai/langchain) 包装 `SparkLLMBase()` ，得到 `Spark()` 类。
 4. `SparkApiTest.py` ：内置了三个小项目。
 5. `1.txt` ：用于试验的小文本。
 6. `error_records.txt` ：遇到的问题记录，不一定能彻底解决，但是起作用了。

## Run

`SparkApiTest.py` 内置了三个小项目，全部运行比较消耗token，可以适当注释几个函数再运行。

```
python SparkApiTest.py
```

## Thanks

 - [讯飞星火认知大模型官网](https://xinghuo.xfyun.cn/)
 - [LangChain 的 Github 主页](https://github.com/langchain-ai/langchain)
 - [CSDN - 川川菜鸟 - 博客](https://blog.csdn.net/weixin_46211269/article/details/131720896)
 - [掘金 - 张冶国zyg - 博客](https://juejin.cn/post/7232272098755723324)
 - [LangChain 中文入门教程 - 小项目支持](https://liaokong.gitbook.io/llm-kai-fa-jiao-cheng/)

## Last

这是最基本、最简单的封装了；可能后续会有官方 or 其他开发者设计更好的封装，开发有趣的小程序～

PS：为什么感觉星火认知大模型的 “记忆” 能力差点？





