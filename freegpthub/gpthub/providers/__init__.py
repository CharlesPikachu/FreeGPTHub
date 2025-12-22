'''initialize'''
from .zhipu import ZhipuGLMEndpoints
from .minimax import MiniMaxEndpoints
from .oai import OpenAIChatGPTEndpoints
from .baidu import BaiduQianfanEndpoints
from .alibaba import AlibabaQwenEndpoints
from .iflytek import IFLYTEKSparkEndpoints
from .bytedance import ByteDanceDoubaoEndpoints
from .base import BaseEndpoint, EndpointRegistry
from .highflyer import HighflyerDeepSeekEndpoints