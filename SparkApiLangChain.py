# 从typing库中导入必要的函数和类型声明
from typing import Any, List, Mapping, Optional

# 导入所需的类和接口
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM

from SparkApiPackaging import SparkLLMBase


# 定义一个名为Spark的子类，继承自LLM类
class Spark(LLM):
    # 类的成员变量
    max_tokens = 1024
    temperature = 0.5
    spark_kernel = SparkLLMBase(max_tokens=max_tokens,
                                temperature=temperature)
    spark_indentify = 'spark'

    # 用于指定该子类对象的类型
    @property
    def _llm_type(self) -> str:
        return "Spark"

    # 重写基类方法，根据用户输入的prompt来响应用户，返回字符串
    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        return self.spark_kernel(prompt)

    # 返回一个字典类型，包含LLM的唯一标识
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"spark": self.spark_indentify}

# # --------------------- test code ---------------------
# if __name__ == "__main__":
#     mySpark = Spark()
#     print(mySpark("请你设计一个中餐厅菜馆的菜单。"))
