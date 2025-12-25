'''initialize'''
from .hema import HeMaProvider
from .baidu import BaiDuProvider
from .qimao import QiMaoProvider
from .weiguan import WeiGuanProvider
from .honggguo import HongGuoProvider
from .base import BaseProvider, Provider
from freegpthub.gpthub.utils.modulebuilder import BaseModuleBuilder


'''ProviderBulder'''
class ProviderBulder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'HeMaProvider': HeMaProvider, 'BaiDuProvider': BaiDuProvider, 'QiMaoProvider': QiMaoProvider,
        'WeiGuanProvider': WeiGuanProvider, 'HongGuoProvider': HongGuoProvider,
    }


'''BuildProvider'''
BuildProvider = ProviderBulder().build