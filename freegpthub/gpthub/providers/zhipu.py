'''
Function:
    Implementation of ZhipuGLMEndpoints
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from .base import BaseEndpoint
from ..utils import ChatRequest, ChatResponse, ModelIOType


'''SETTINGS'''
GLM_FREE_API_V4_KEYS = {
    'glm-4-flash': [
        '41FBx1_ZwnT1-60C4MqbIkC7JZDBjbWEeoIYF_Oiiqct6D76bN5UUNSE3WjBWiC6RK0WGqU18-gu2ibOsHqoh1WEhzfXbMrmDlz8jpjTWcpsNvPXT8HeP4uVhuielvFI', 
        'g48qv0w9UpBhhhS4_4Pll844fO5SgHKSQStWnjzrzaveW-uwhMUWEak7LhRs-zMVJbXNPB2m3gsvSTnSd-cos8qk1yMV0X_i77yUqgPWN9wDGXgysETY5q09DtDKY_AR', 
        'iJguE3LqmI0AVxD6jqa0reYaHzUz2c7WMnKNcT0MONVuuuIobBJ5pqVC9Eu6Mu2iCJ-guc2b-6dmUNytDjW2PKiNW48pf920newsQtFoPCTUrklhakq-tz7jyvFQ7Hol', 
        '2WgmiDRi7g54Yyk_YPxv0i0MJFDOlyMrPfFwuYAK4YvVU774Zcx5BtAmr2JTkygYp7ZfCprP6tp1l2w6QpOGReB9ATRLIbsRELr36GVImVrJqGtV5csNMBO4OqhEp5eT', 
        'O168BowcawcXE-lUKVJx2bX4pwffPG0zp23jWolVd-IbhdN4XP8LAb6DyKbu_GZTxKPPkpeuCRtE-jRwzTh5KgGCMR4PUkMHkwtY-XlepIxlHhFEp8Jrgni_KnvEsEs2', 
        'BRDl_p4-kbu7I8o9DQi_TZodSuRb_ytpZEKGlRbneF8VNWGIjgU9WwsnN9WfSmo484ryXlnzDJS3tuZ4jtWQNkitsoZZ7OUaWA646Nueszd4PXUeij1r6wDaWS0YdFRh', 
        'tt8c_3Y1gEVwjLa6eSgA4-cjI1TWQTHHFhLo2ju7l4UTXkZghQVFwff-Wf2-en6pM6hZcJ4T28x0fXEkGDEdVRGHzcU-SsnDNK9wu0oLROmt6_7L3vOz3kOdVkX0kbQY', 
        'KGoKIMwCt-fzCeRsGaR56HYg6RnDeAppnQKL0ygCz55-GWC2uemKz727siMKH5B5jRv-Dg5siTmO7nx-MS2wW-D50--V-uLnp3tHhoDDI8ta1C9yUWy1Q56RgHOcGNes', 
        'n9IzbV6URId290jgrTdPbRurYt2kDO3RDQzgX-B_tbHUNqbGpNoBHqxHQiz8gDiZgPWekA07kp7l1aywVGawGQlf7AyUkOjV43s6vG8pT7blhgox488Y6Zrhsg-e6wj-', 
        'HFFuMzZ9mE7MUGD_ysP6ZiEPkANBN2iRyAapZYY08VdyAlKd327GWtZUEG6lqZBHjlfCYCtQrACmDqK8GrMYm2JKbiYe7hwtDYQUizTnnP_GyWT2dAf8w2rfHAvfnUSK', 
        'gAYd6e3XCqJ0tEIIFiPxSM7q_VCD22E3Hjl9alLNwHEvLtjyxJ0x4wjsd54psEPfo1hCnIKTbCmfybsN0OrYBnOg54nsKiGyShjq6zyBkXyHHq3lFRM4gDnXIuXryuXq',
    ], 
    'glm-4.5-flash': [
        '41FBx1_ZwnT1-60C4MqbIkC7JZDBjbWEeoIYF_Oiiqct6D76bN5UUNSE3WjBWiC6RK0WGqU18-gu2ibOsHqoh1WEhzfXbMrmDlz8jpjTWcpsNvPXT8HeP4uVhuielvFI', 
        'g48qv0w9UpBhhhS4_4Pll844fO5SgHKSQStWnjzrzaveW-uwhMUWEak7LhRs-zMVJbXNPB2m3gsvSTnSd-cos8qk1yMV0X_i77yUqgPWN9wDGXgysETY5q09DtDKY_AR', 
        'iJguE3LqmI0AVxD6jqa0reYaHzUz2c7WMnKNcT0MONVuuuIobBJ5pqVC9Eu6Mu2iCJ-guc2b-6dmUNytDjW2PKiNW48pf920newsQtFoPCTUrklhakq-tz7jyvFQ7Hol', 
        '2WgmiDRi7g54Yyk_YPxv0i0MJFDOlyMrPfFwuYAK4YvVU774Zcx5BtAmr2JTkygYp7ZfCprP6tp1l2w6QpOGReB9ATRLIbsRELr36GVImVrJqGtV5csNMBO4OqhEp5eT', 
        'O168BowcawcXE-lUKVJx2bX4pwffPG0zp23jWolVd-IbhdN4XP8LAb6DyKbu_GZTxKPPkpeuCRtE-jRwzTh5KgGCMR4PUkMHkwtY-XlepIxlHhFEp8Jrgni_KnvEsEs2', 
        'BRDl_p4-kbu7I8o9DQi_TZodSuRb_ytpZEKGlRbneF8VNWGIjgU9WwsnN9WfSmo484ryXlnzDJS3tuZ4jtWQNkitsoZZ7OUaWA646Nueszd4PXUeij1r6wDaWS0YdFRh', 
        'tt8c_3Y1gEVwjLa6eSgA4-cjI1TWQTHHFhLo2ju7l4UTXkZghQVFwff-Wf2-en6pM6hZcJ4T28x0fXEkGDEdVRGHzcU-SsnDNK9wu0oLROmt6_7L3vOz3kOdVkX0kbQY', 
        'KGoKIMwCt-fzCeRsGaR56HYg6RnDeAppnQKL0ygCz55-GWC2uemKz727siMKH5B5jRv-Dg5siTmO7nx-MS2wW-D50--V-uLnp3tHhoDDI8ta1C9yUWy1Q56RgHOcGNes', 
        'n9IzbV6URId290jgrTdPbRurYt2kDO3RDQzgX-B_tbHUNqbGpNoBHqxHQiz8gDiZgPWekA07kp7l1aywVGawGQlf7AyUkOjV43s6vG8pT7blhgox488Y6Zrhsg-e6wj-', 
        'HFFuMzZ9mE7MUGD_ysP6ZiEPkANBN2iRyAapZYY08VdyAlKd327GWtZUEG6lqZBHjlfCYCtQrACmDqK8GrMYm2JKbiYe7hwtDYQUizTnnP_GyWT2dAf8w2rfHAvfnUSK', 
        'gAYd6e3XCqJ0tEIIFiPxSM7q_VCD22E3Hjl9alLNwHEvLtjyxJ0x4wjsd54psEPfo1hCnIKTbCmfybsN0OrYBnOg54nsKiGyShjq6zyBkXyHHq3lFRM4gDnXIuXryuXq',
    ],
}


'''ZhipuGLMEndpoints'''
class ZhipuGLMEndpoints(BaseEndpoint):
    provider, model = "zhipu", "glm"
    def __init__(self, **kwargs):
        super(ZhipuGLMEndpoints, self).__init__(**kwargs)
        for ver in list(GLM_FREE_API_V4_KEYS.keys()):
            self.registervariant(ver, io_supported=[ModelIOType.fromtag("T2T")])
            self.registerapi(
                version=ver, name="officialapiv4", io=ModelIOType.fromtag("T2T"), handler="officialapiv4",
                priority=100, note='official api: https://open.bigmodel.cn/api/paas/v4/'
            )
    '''officialapiv4'''
    def officialapiv4(self, req: ChatRequest, request_overrides: dict = None, version: str = None) -> ChatResponse:
        return self.openaisdk(
            base_url='https://open.bigmodel.cn/api/paas/v4/', candidate_api_keys=GLM_FREE_API_V4_KEYS, api_family='client.chat.completions.create',
            req=req, request_overrides=request_overrides, version=version
        )