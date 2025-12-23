'''
Function:
    Implementation of ModelScopeEndpoints
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from ..providers import BaseEndpoint
from ..utils import ChatRequest, ChatResponse, ModelIOType, Modality


'''SETTINGS'''
MODELSCOPE_FREE_SHARED_KEYS = [
    'd8piqH1om7slDpWVFr9fABSIFM3XCG2Ra4SMy_tfjnklvf9UqO6_ihRsGxTeobKIJEY8F-nmAsYFkKOPuOOfdB5SmwLGaVRobr-WYcsuNz4=', 
    'oydsr5t5wmt-rOSTfatD3XtYBzfRFFpnHzrr4NlUBPkSkEqEqGhOEuyPQ4ktEV6w2lfKjDzFKkLBgaAQXEkfAoQpNdA0lbwSw6VbjLyCLNA=', 
    'YtNDaEMdeCCcKi-Yy1sSi6o-lfz5hzSLog8mANsIdIKzLZzaD4X8Da_5mCAzMfNVkJvh6rwsBfRiSh6R9TWdH4T26rM6x5JRLlXb6oITkLk=', 
    '__ZVhAz8E8DaFnvPEA5zOSaq_GckwEWMhrjs2CIUPx6REQpiZNFsgIK6isg7GhewToXfXgd6Iz9oXWUrZG28SdYJUDfMqRAKqHvKtIMmScQ=', 
    '_DdGpBoqyuFvDRIta6S1UhtjrmED9fI2ZY3kHR2ama4PWsMp49z4sAce-fqHevqF0XXAYHLVxcz_hjYGyzWHg0YElNdlw0VOveFmiRsWdqI=', 
    'pHZF58cVvgZAniBVIrcvwQQ-S7TmBzqf4N901Xpu0IGX-HFmviIiAUuMqXUKi4JhvF5dG8W3C8TRNQcjQGoFq2UwfQl6iW_KdqvWYRNTf7w=', 
    'XS67Yk6npZKPd9BeE-Z7ukUBylE9wlCFhNguP78MlxoTYv3M1hcctcLfNEcrfsSHnT88VT0MWQfCbjvF7exTBP4c80wCuyq-ca9coc2VqtE=', 
    'SGa6z9tEpQpILJ4irk7-mvC8DUHSnRf8CS1upuNdzyDQoITLDnnaml_l8F7V_fYzBYrGHvbLJ-TDKojqO3iPyoJpEJZGzoWZg4gikvLpD4Y=', 
    'L0Qsd768J0yA5Ko_DIdVcluFSJcDmSROBXjTaj9p33R0IZ5EIQ3ihKshMUd2UyzubJFTySSw2nLMA2WVxnzbsP1ckMAu--z7MuHtt-f88s8=', 
    'f3EKoSKBfLAfxmF2faH7T9zWziG0V-Bm4XaDZgEdsBgfKoQFo-7HuggxK4dXmmRiF1AmIeNel65mU4bsJ-FY7hQPEd9NMCHdqTv4_WGRwGM=', 
    'xrufyy485ATw0B_gjX7WHowLGlbmUSapivx2t0nXuSy7DEQTofKV6-Dahc1_TVNFgEtcDd6xpFj3CPNq3rWEipqV-VVrhbCvxU4BFsQ2NYs=', 
    '0cKSIfmeU08Ta9QY9sQWb8Rl5xW4vR2ktVpPcdXa82HonK0L6Fz23kJO7sb_4zTjhCS1Sw_UjxqNImAUT3uioN_zUcEkViv7s3DIptI3w3Q=', 
    '7RwLU4FOqfvJcgOlX9csIhcYpK94DeJTnb13Xk0Nol_9OjgABW4Xc6VElB3ucl5XEkW8oqqBMIVtGp4eMB5uQt-0eMCD5pKPkhFwUx8v5Vg=', 
    '_DG9pFj8UGd4R1UEXj1Z623TPiEWIl2aolwkuuRD1P_JA6WqUnIbiYUQM-Ic1mqOkYkgMDIhvpjipeajNcmFZhMMTG1A3RqVKUhbQ1i3Qvg=', 
    'C-4l68NbnLfOnJ3ygysIKjQy-j43qhZymt0SWCxnnel4QpLrH3oU45v2n1bU_i2UrC42PMbA-HxYKzlgt2BcWvNJaFDYxOMc4fGsVPPr2CM=', 
    'zK-WLS_jjbdJM789aUPaqBwQiUroNqn8OMSFGehv1gyentkX-94on_XXlOqf6NBbCbQ9Djc6SueKwQuiAfW9iqzkEMgIWIsOJ_2AL1sdtiQ=', 
    'X6Q0dRVwgRuOpZLqy9hx5UcWK9_Ie4D4VPRXQn8F-kBtR_6cW5XabAmsyiyJ5Pu2OnlxFhi56SeR8xpVPHL5K25LY_qnJv3QsDMiyVIh2CE=',
]
MODELSCOPE_FREE_MODEL_IDS = [
    'deepseek-ai/DeepSeek-R1-0528', 'deepseek-ai/DeepSeek-R1-Distill-Llama-70B', 'deepseek-ai/DeepSeek-R1-Distill-Llama-8B', 'deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', 'deepseek-ai/DeepSeek-R1-Distill-Qwen-14B', 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B', 'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B', 'deepseek-ai/DeepSeek-V3.2', 
    'LLM-Research/c4ai-command-r-plus-08-2024', 'LLM-Research/Llama-4-Maverick-17B-128E-Instruct', 
    'Menlo/Jan-nano', 'MiniMax/MiniMax-M1-80k', 
    'mistralai/Ministral-8B-Instruct-2410', 'mistralai/Mistral-Large-Instruct-2407', 'mistralai/Mistral-Small-Instruct-2409', 
    'MusePublic/Qwen-Image-Edit', 
    'opencompass/CompassJudger-1-32B-Instruct', 
    'OpenGVLab/InternVL3_5-241B-A28B', 
    'PaddlePaddle/ERNIE-4.5-0.3B-PT', 'PaddlePaddle/ERNIE-4.5-21B-A3B-PT', 'PaddlePaddle/ERNIE-4.5-300B-A47B-PT', 'PaddlePaddle/ERNIE-4.5-VL-28B-A3B-PT', 
    'Qwen/QVQ-72B-Preview', 'Qwen/Qwen-Image-Edit', 'Qwen/Qwen2.5-14B-Instruct', 'Qwen/Qwen2.5-14B-Instruct-1M', 'Qwen/Qwen2.5-32B-Instruct', 'Qwen/Qwen2.5-72B-Instruct', 'Qwen/Qwen2.5-7B-Instruct', 'Qwen/Qwen2.5-7B-Instruct-1M', 'Qwen/Qwen2.5-Coder-14B-Instruct', 'Qwen/Qwen2.5-Coder-32B-Instruct', 'Qwen/Qwen2.5-Coder-7B-Instruct', 'Qwen/Qwen2.5-VL-32B-Instruct', 'Qwen/Qwen2.5-VL-3B-Instruct', 'Qwen/Qwen2.5-VL-72B-Instruct', 'Qwen/Qwen2.5-VL-7B-Instruct', 'Qwen/Qwen3-0.6B', 'Qwen/Qwen3-1.7B', 'Qwen/Qwen3-14B', 'Qwen/Qwen3-235B-A22B', 'Qwen/Qwen3-235B-A22B-Instruct-2507', 'Qwen/Qwen3-235B-A22B-Thinking-2507', 'Qwen/Qwen3-30B-A3B', 'Qwen/Qwen3-30B-A3B-Thinking-2507', 'Qwen/Qwen3-32B', 'Qwen/Qwen3-4B', 'Qwen/Qwen3-8B', 'Qwen/Qwen3-Coder-30B-A3B-Instruct', 'Qwen/Qwen3-Coder-480B-A35B-Instruct', 'Qwen/Qwen3-Next-80B-A3B-Instruct', 'Qwen/Qwen3-Next-80B-A3B-Thinking', 'Qwen/Qwen3-VL-235B-A22B-Instruct', 'Qwen/Qwen3-VL-8B-Instruct', 'Qwen/Qwen3-VL-8B-Thinking', 'Qwen/QwQ-32B', 'Qwen/QwQ-32B-Preview', 
    'Shanghai_AI_Laboratory/Intern-S1', 'Shanghai_AI_Laboratory/Intern-S1-mini', 
    'stepfun-ai/step3', 
    'XGenerationLab/XiYanSQL-QwenCoder-32B-2412', 'XGenerationLab/XiYanSQL-QwenCoder-32B-2504', 
    'XiaomiMiMo/MiMo-V2-Flash'
]
MODELSCOPE_FREE_TI_MODEL_IDS = [
    "LLM-Research/Llama-4-Maverick-17B-128E-Instruct",
    "OpenGVLab/InternVL3_5-241B-A28B",
    "PaddlePaddle/ERNIE-4.5-VL-28B-A3B-PT",
    "Qwen/QVQ-72B-Preview", "Qwen/Qwen2.5-VL-32B-Instruct", "Qwen/Qwen2.5-VL-3B-Instruct", "Qwen/Qwen2.5-VL-72B-Instruct", "Qwen/Qwen2.5-VL-7B-Instruct", "Qwen/Qwen3-VL-235B-A22B-Instruct", "Qwen/Qwen3-VL-8B-Instruct", "Qwen/Qwen3-VL-8B-Thinking",
    "stepfun-ai/step3",
]
MODELSCOPE_FREE_API_V1_KEYS = {}
for model_id in MODELSCOPE_FREE_MODEL_IDS: MODELSCOPE_FREE_API_V1_KEYS[model_id] = MODELSCOPE_FREE_SHARED_KEYS


'''ModelScopeEndpoints'''
class ModelScopeEndpoints(BaseEndpoint):
    provider, model = "modelscope", "common"
    def __init__(self, **kwargs):
        super(ModelScopeEndpoints, self).__init__(**kwargs)
        TI2T = ModelIOType.create(inputs=[Modality.TEXT, Modality.IMAGE], outputs=[Modality.TEXT])
        for ver in list(MODELSCOPE_FREE_API_V1_KEYS.keys()):
            if ver in MODELSCOPE_FREE_TI_MODEL_IDS:
                self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T"), TI2T])
                self.registerapi(
                    version=ver, name="officialapiv1", io=ModelIOType.fromtag("T2T"), handler="officialapiv1",
                    priority=100, note='official api: https://api-inference.modelscope.cn/v1'
                )
                self.registerapi(
                    version=ver, name="visionofficialapiv1", io=TI2T, handler="visionofficialapiv1", priority=100, note='official api: https://api-inference.modelscope.cn/v1'
                )
            else:
                self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")])
                self.registerapi(
                    version=ver, name="officialapiv1", io=ModelIOType.fromtag("T2T"), handler="officialapiv1",
                    priority=100, note='official api: https://api-inference.modelscope.cn/v1'
                )
    '''officialapiv1'''
    def officialapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://api-inference.modelscope.cn/v1', candidate_api_keys=MODELSCOPE_FREE_API_V1_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )
    '''visionofficialapiv1'''
    def visionofficialapiv1(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.visionopenaisdk(
            base_url='https://api-inference.modelscope.cn/v1', candidate_api_keys=MODELSCOPE_FREE_API_V1_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )