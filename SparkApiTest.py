from SparkApiLangChain import Spark
from langchain.prompts import PromptTemplate
from langchain.chains import LLMRequestsChain, LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import SimpleSequentialChain

spark = Spark(max_tokens=2048)


# --------------------- test code 1 ---------------------
def test_code_1():
    print(spark("What can you do?"))


# --------------------- test code 2 ---------------------
def test_code_2():
    template = """在 >>> 和 <<< 之间是网页的返回的HTML内容。
    网页是新浪财经A股上市公司的公司简介。
    请抽取参数请求的信息。

    >>> {requests_result} <<<
    请使用如下的JSON格式返回数据
    {{
      "company_name":"a",
      "company_english_name":"b",
      "issue_price":"c",
      "date_of_establishment":"d",
      "registered_capital":"e",
      "office_address":"f",
      "Company_profile":"g"

    }}
    Extracted:"""

    prompt = PromptTemplate(
        input_variables=["requests_result"],
        template=template
    )

    chain = LLMRequestsChain(llm_chain=LLMChain(llm=spark, prompt=prompt))
    inputs = {
        "url": "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/600519.phtml"
    }

    response = chain(inputs)
    print(response['output'])


# --------------------- test code 3 ---------------------
def test_code_3():
    # 导入文本
    loader = TextLoader("./1.txt")
    # 将文本转成 Document 对象
    document = loader.load()

    # 初始化文本分割器
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=256,
                                                   chunk_overlap=16)

    # 切分文本
    splitted_documents = text_splitter.split_documents(document)

    # 创建总结链
    Chain_instance = load_summarize_chain(llm=spark,
                                          chain_type='refine',
                                          verbose=True)

    # 执行总结链，（为了快速演示，只总结前5段）
    response = Chain_instance.run(splitted_documents[:])
    print(response)


# --------------------- test code 4 ---------------------
def test_code_4():
    # location 链
    template = """
    Your job is to come up with a classic dish from the area that the users suggests.
    % USER LOCATION
    {user_location}

    YOUR RESPONSE:
    """

    prompt_template = PromptTemplate(input_variables=['user_location'], template=template)

    location_chain = LLMChain(llm=spark, prompt=prompt_template)

    # meal 链
    template = """Given a meal, give a short and simple recipe on how to make that dish at home.
    % MEAL
    {user_meal}

    YOUR RESPONSE:
    """

    prompt_template = PromptTemplate(input_variables=["user_meal"], template=template)

    meal_chain = LLMChain(llm=spark, prompt=prompt_template)
    # 通过 SimpleSequentialChain 串联起来，第一个答案会被替换第二个中的user_meal，然后再进行询问
    overall_chain = SimpleSequentialChain(chains=[location_chain, meal_chain], verbose=True)
    review = overall_chain.run("Rome")
    return review


if __name__ == "__main__":
    print("************ test 1 ************")
    print(test_code_1())
    print("\n")
    print("************ test 2 ************")
    print(test_code_2())
    print("\n")
    print("************ test 3 ************")
    print(test_code_3())
    print("\n")
    print("************ test 4 ************")
    print(test_code_4())
    print("\n")
