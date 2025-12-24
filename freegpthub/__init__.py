'''title'''
__title__ = 'freegpthub'
'''description'''
__description__ = 'FreeGPTHub: A truly free, unified GPT API gateway—unlike “fake-free” alternatives that hide paywalls behind quotas, trials, or mandatory top-ups.'
'''url'''
__url__ = 'https://github.com/CharlesPikachu/FreeGPTHub'
'''version'''
__version__ = '0.1.0'
'''author'''
__author__ = 'Zhenchao Jin'
'''email'''
__email__ = 'charlesblwx@gmail.com'
'''license'''
__license__ = 'Apache License 2.0'
'''copyright'''
__copyright__ = 'Copyright 2025-2030 Zhenchao Jin'


'''init'''
from .registered import REGISTERED_ENDPOINTS
from .gpthub import (
    ModelIOType, Modality, ChatRequest, ChatResponse, APISpec, ModelVariant, SecretUtils, StreamSanitizer,
    BaseEndpoint, EndpointRegistry, IFLYTEKSparkEndpoints, BaiduQianfanEndpoints, OpenAIChatGPTEndpoints, ZhipuGLMEndpoints,
    HighflyerDeepSeekEndpoints, ByteDanceDoubaoEndpoints, AlibabaQwenEndpoints, MiniMaxEndpoints, ModelScopeEndpoints,
)